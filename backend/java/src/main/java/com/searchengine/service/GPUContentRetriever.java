package com.searchengine.service;

import com.searchengine.model.SearchResult;
import org.springframework.stereotype.Service;
import javax.annotation.PostConstruct;
import java.util.concurrent.*;
import java.util.*;
import java.util.stream.Collectors;
import java.io.*;

import com.opencsv.CSVParserBuilder;
import com.opencsv.CSVReader;
import com.opencsv.CSVReaderBuilder;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


@Service
public class GPUContentRetriever {
    private static final Logger logger = LoggerFactory.getLogger(GPUContentRetriever.class);
    private static final Map<String, List<String[]>> DATASET_CACHE = new ConcurrentHashMap<>();
    private static final Map<String, Map<String, Integer>> DATASET_COLUMNS = new ConcurrentHashMap<>();
    private static final Map<String, String> DATASET_PATHS = new ConcurrentHashMap<>();
    private static final int BATCH_SIZE = 10000;
    private static final int THREAD_POOL_SIZE = Runtime.getRuntime().availableProcessors();
    private final Map<String, Map<Integer, String[]>> indexedDatasets = new ConcurrentHashMap<>();
    private final ExecutorService executorService = Executors.newFixedThreadPool(THREAD_POOL_SIZE);
    private static final int PAGE_SIZE = 100;

    @PostConstruct
    public void initialize() {
        try {
            initializeDatasetMappings();
            preloadDatasets();
        } catch (Exception e) {
            logger.error("Failed to initialize: {}", e.getMessage());
            throw new RuntimeException("Initialization failed", e);
        }
    }

    private static final Map<String, int[]> DATASET_RANGES = new ConcurrentHashMap<>() {{
        put("GlobalNewsDataset", new int[]{1000000, 1105351});
        put("RedditDataset", new int[]{1105352, 1519554});
        put("WeeklyNewsDataset_Aug17", new int[]{1519555, 1979142});
        put("WeeklyNewsDataset_Aug18", new int[]{1979143, 2455685});
    }};

    private void preloadDatasets() {
        DATASET_PATHS.forEach((name, path) -> {
            List<String[]> data = loadDataset(path);
            indexDataset(name, data);
            logger.info("Preloaded and indexed dataset: {}", name);
        });
    }

    private void indexDataset(String datasetName, List<String[]> data) {
        Map<Integer, String[]> indexed = new ConcurrentHashMap<>();
        data.parallelStream().forEach(line -> {
            try {
                int docId = Integer.parseInt(line[0].trim());
                indexed.put(docId, line);
            } catch (NumberFormatException e) {
                logger.warn("Invalid docId in line: {}", line[0]);
            }
        });
        
        indexedDatasets.put(datasetName, indexed);
    }

    private void initializeDatasetMappings() {
        File projectDir = new File(System.getProperty("user.dir"))
            .getParentFile()
            .getParentFile();
            
        String dataPath = new File(projectDir, "data").getAbsolutePath();
        
        // Initialize all dataset paths
        // DATASET_PATHS.put("GlobalNewsDataset", 
        //     new File(dataPath, "SampleDatasets_ForTesting/GlobalNewsDataset_Sample_5000.csv").getAbsolutePath());
        // DATASET_PATHS.put("RedditDataset", 
        //     new File(dataPath, "SampleDatasets_ForTesting/RedditDataset_Sample_5000.csv").getAbsolutePath());
        // DATASET_PATHS.put("WeeklyNewsDataset_Aug17", 
        //     new File(dataPath, "SampleDatasets_ForTesting/WeeklyNewsDataset_Aug17_5000.csv").getAbsolutePath());
        // DATASET_PATHS.put("WeeklyNewsDataset_Aug18", 
        //     new File(dataPath, "SampleDatasets_ForTesting/WeeklyNewsDataset_Aug18_5000.csv").getAbsolutePath());
        
        DATASET_PATHS.put("GlobalNewsDataset", 
            new File(dataPath, "Testing/GlobalNewsDataset_Testing.csv").getAbsolutePath());
        DATASET_PATHS.put("RedditDataset", 
            new File(dataPath, "Testing/RedditDatabase_Testing.csv").getAbsolutePath());
        DATASET_PATHS.put("WeeklyNewsDataset_Aug17", 
            new File(dataPath, "Testing/WeeklyNewsDataset_Aug17_Testing.csv").getAbsolutePath());
        DATASET_PATHS.put("WeeklyNewsDataset_Aug18", 
            new File(dataPath, "Testing/WeeklyNewsDataset_Aug18_Testing.csv").getAbsolutePath());
        

        // Initialize all column mappings
        DATASET_COLUMNS.put("GlobalNewsDataset", new HashMap<>() {{
            put("title", 4);              // title       
            put("description", 5);        // description
            put("source", 2);             // source_name 
            put("url", 6);                // url          
        }});
        
        DATASET_COLUMNS.put("RedditDataset", new HashMap<>() {{
            put("title", 3);            // title
            put("description", 3);      // title
            put("source", 2);           // subreddit
            put("url", 7);              // url
            put("score", 8);            // Score
            put("num_comments", 9);     // num_comments
        }});
        
        DATASET_COLUMNS.put("WeeklyNewsDataset_Aug17", new HashMap<>() {{
            put("title", 4);            // headline_text
            put("description", 4);      // headline_text
            put("source", 2);           // feed_code
            put("url", 3);              // source_url
        }});
        
        DATASET_COLUMNS.put("WeeklyNewsDataset_Aug18", new HashMap<>() {{
            put("title", 4);           // headline_text 
            put("description", 4);      // headline_text
            put("source", 2);           // feed_code
            put("url", 3);              // source_url
        }});
        
        logger.info("Initialized all dataset paths and column mappings");
    }

    private String identifyDataset(int docId) {
        for (Map.Entry<String, int[]> entry : DATASET_RANGES.entrySet()) {
            int[] range = entry.getValue();
            if (docId >= range[0] && docId <= range[1]) {
                return entry.getKey();
            }
        }
        return null;
    }

    public List<Integer> filterDocIdsByDataset(List<Integer> docIds, String... datasets) {
        // Create set of allowed datasets for O(1) lookup
        Set<String> allowedDatasets = new HashSet<>(Arrays.asList(datasets));
        System.out.println("running");
        return docIds.parallelStream()
            .filter(docId -> {
                String datasetName = identifyDataset(docId);
                return datasetName != null && allowedDatasets.contains(datasetName);
            })
            .collect(Collectors.toList());
    }

    private SearchResult createSearchResult(int docId, String[] line, Map<String, Integer> columnMap) {
        SearchResult result = new SearchResult();
        result.setDocId(docId);
        try {
            result.setTitle(line[columnMap.get("title")]);
            result.setDescription(line[columnMap.get("description")]);
            result.setUrl(line[columnMap.get("url")]);
            result.setSource(line[columnMap.get("source")]);
            
            String datasetName = identifyDataset(docId);
            if (datasetName != null && datasetName.equals("RedditDataset")) {
                result.setIsReddit(true);
                try {
                    String scoreStr = line[columnMap.get("score")];
                    String commentsStr = line[columnMap.get("num_comments")];
                    
                    // Parse as double first then convert to int
                    int score = (int) Double.parseDouble(scoreStr.trim());
                    int numComments = (int) Double.parseDouble(commentsStr.trim());
                    
                    result.setScore(score);
                    result.setNumComments(numComments);
                } catch (NumberFormatException e) {
                    logger.error("Error parsing Reddit metrics for DocID {}: {}", docId, e.getMessage());
                    result.setScore(0);
                    result.setNumComments(0);
                }
            }
        } catch (Exception e) {
            logger.error("Error creating search result for docId {}: {}", docId, e.getMessage());
        }
        return result;
    }
    private List<String[]> loadDataset(String path) {
        return DATASET_CACHE.computeIfAbsent(path, k -> {
            logger.info("Loading dataset from: {}", k);
            try {
                if (k.contains("RedditDataset")) {
                    CSVReader reader = new CSVReaderBuilder(new FileReader(k))
                        .withCSVParser(new CSVParserBuilder()
                            .withSeparator(',')
                            .withQuoteChar('"')
                            .withEscapeChar('\\')
                            .withStrictQuotes(false)
                            .build())
                        .withSkipLines(1)
                        .build();
                    
                    List<String[]> data = reader.readAll()
                        .stream()
                        .filter(line -> {
                            try {
                                return line != null && 
                                       line.length >= 8 && 
                                       line[0] != null && 
                                       line[0].trim().matches("^\\d{7}$");
                            } catch (Exception e) {
                                return false;
                            }
                        })
                        .collect(Collectors.toList());
                    
                    logger.info("Loaded {} valid rows from Reddit dataset", data.size());
                    return data;
                } else {
                    // Original code for other datasets
                    CSVReader reader = new CSVReader(new FileReader(k));
                    reader.skip(1);
                    List<String[]> data = reader.readAll();
                    logger.info("Loaded {} rows from dataset", data.size());
                    return data;
                }
            } catch (Exception e) {
                return new ArrayList<>();
            }
        });
    }

    public List<Object> getContentGPU(List<Integer> docIds, int page) {
        if (docIds == null || docIds.isEmpty()) {
            return Arrays.asList(Collections.emptyList(), 0);
        }
    
        // String[] redditDataset = {
        //     "GlobalNewsDataset"
        // };
        
        // docIds = filterDocIdsByDataset(docIds, redditDataset);
        int totalFilteredResults = docIds.size();
    
        // Calculate pagination bounds
        int startIndex = (page - 1) * PAGE_SIZE;
        int endIndex = Math.min(startIndex + PAGE_SIZE, docIds.size());
        
        // Get subset of docIds for current page
        List<Integer> pageDocIds = docIds.subList(startIndex, endIndex);
    
        // Process page batch
        List<SearchResult> results = pageDocIds.parallelStream()
            .collect(Collectors.groupingBy(id -> id / BATCH_SIZE))
            .values()
            .parallelStream()
            .map(batch -> processBatch(batch))
            .flatMap(Collection::stream)
            .collect(Collectors.toList());

        results.sort(Comparator.comparingInt(result -> 
            pageDocIds.indexOf(result.getDocId())));
    
        return Arrays.asList(results, totalFilteredResults);
    }

    // Add method to get total results count
    public int getTotalResults(List<Integer> docIds) {
        return docIds != null ? docIds.size() : 0;
    }

    private List<SearchResult> processBatch(List<Integer> batch) {

        return batch.parallelStream()
            .map(docId -> {
                String datasetName = identifyDataset(docId);

                if (datasetName == null) return null;
                Map<Integer, String[]> dataset = indexedDatasets.get(datasetName);
                if (dataset == null) return null;
                String[] line = dataset.get(docId);

                if (line == null) return null;
                return createSearchResult(docId, line, DATASET_COLUMNS.get(datasetName));
            })
            .filter(Objects::nonNull)
            .collect(Collectors.toList());
    }
}