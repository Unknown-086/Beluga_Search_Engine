package com.searchengine.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;
import com.searchengine.model.SearchResult;
import com.searchengine.service.GPUContentRetriever;
import org.springframework.stereotype.Service;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import javax.annotation.PostConstruct;
import java.io.*;
import java.util.*;
import com.opencsv.CSVReader;
import com.opencsv.CSVReaderBuilder;


@Service
public class SearchService {
    private static final Logger logger = LoggerFactory.getLogger(SearchService.class);
    private final GPUContentRetriever gpuContentRetriever;
    private final String basePath;
    private final String lexiconPath;
    private final String barrelMetadataPath;

    public SearchService(GPUContentRetriever gpuContentRetriever) {
        this.gpuContentRetriever = gpuContentRetriever;
        
        File projectDir = new File(System.getProperty("user.dir"))
            .getParentFile()
            .getParentFile();
        
        this.basePath = new File(projectDir, "data").getAbsolutePath();
        this.lexiconPath = new File(basePath, "Lexicons/Testing/Lexicon_Testing.json").getAbsolutePath();
        this.barrelMetadataPath = new File(basePath, "BarrelData/Testing/PathData/Barrels_Testing_Metadata.json").getAbsolutePath();
        
        createDirectoriesIfNeeded();
        verifyPaths();
    }
    
    private void createDirectoriesIfNeeded() {
        new File(lexiconPath).getParentFile().mkdirs();
        new File(barrelMetadataPath).getParentFile().mkdirs();
    }

    // private static final Map<String, int[]> DATASET_RANGES = new HashMap<>() {{
    //     put("GlobalNewsDataset", new int[]{1000000, 1105351});
    //     put("RedditDataset", new int[]{1105352, 1519554});
    //     put("WeeklyNewsDataset_Aug17", new int[]{1519555, 1979142});
    //     put("WeeklyNewsDataset_Aug18", new int[]{1979143, 2455685});
    // }};

    private void verifyPaths() {
        if (!new File(lexiconPath).exists()) {
            throw new RuntimeException("Lexicon file not found: " + lexiconPath);
        }
        if (!new File(barrelMetadataPath).exists()) {
            throw new RuntimeException("Barrel metadata file not found: " + barrelMetadataPath);
        }
    }

    private static final Map<String, String> DATASET_PATHS = new HashMap<>();
    
    @PostConstruct
    private void initializePaths() {
        DATASET_PATHS.put("GlobalNewsDataset", new File(basePath, "Testing/GlobalNewsDataset_Testing.csv").getAbsolutePath());
        DATASET_PATHS.put("RedditDataset", new File(basePath, "Testing/RedditDatabase_Testing.csv").getAbsolutePath());
        DATASET_PATHS.put("WeeklyNewsDataset_Aug17", new File(basePath, "Testing/WeeklyNewsDataset_Aug17_Testing.csv").getAbsolutePath());
        DATASET_PATHS.put("WeeklyNewsDataset_Aug18", new File(basePath, "Testing/WeeklyNewsDataset_Aug18_Testing.csv").getAbsolutePath());
    }


    // private static final Map<String, Map<String, Integer>> DATASET_COLUMNS = new HashMap<>() {{
    //     put("GlobalNewsDataset", new HashMap<>() {{
    //         put("title", 4);          // title         
    //         put("description", 5);     // description 
    //         put("source", 2);         // source_name  
    //         put("url", 6);           // url           
    //     }});
        
    //     put("RedditDataset", new HashMap<>() {{
    //         put("title", 3);          // title
    //         put("description", 3);     // title
    //         put("source", 2);         // subreddit
    //         put("url", 7);           // url
    //     }});
        
    //     put("WeeklyNewsDataset_Aug17", new HashMap<>() {{
    //         put("title", 4);          // headline_text
    //         put("description", 4);     // headline_text
    //         put("source", 2);         // feed_code
    //         put("url", 3);           // source_url
    //     }});
        
    //     put("WeeklyNewsDataset_Aug18", new HashMap<>() {{
    //         put("title", 4);          // headline_text
    //         put("description", 4);     // headline_text
    //         put("source", 2);         // feed_code
    //         put("url", 3);           // source_url
    //     }});
    // }};

    private String resolveBarrelPath(String relativePath) {
        if (relativePath.startsWith("../")) {
            // Convert relative path to absolute
            File projectRoot = new File(System.getProperty("user.dir"))
                .getParentFile()  // java
                .getParentFile(); // backend
            return new File(projectRoot, relativePath.replace("../..", "")).getAbsolutePath();
        }
        return relativePath;
    }

    public Map<String, Object> search(String query, int page) {
        // Add debug logging
        logger.info("Starting search for query: {} page: {}", query, page);
        
        int wordId = getLexiconWordId(query.toLowerCase());
        if (wordId == 0) return createEmptyResponse();
        
        String barrelPath = getBarrelPath(wordId);
        if (barrelPath.isEmpty()) return createEmptyResponse();
        
        List<Integer> docIds = getDocIds(barrelPath, wordId);
        int totalResults = docIds.size();
        
        // Add debug logging
        logger.info("Found {} total results", totalResults);
        
        List<SearchResult> results = gpuContentRetriever.getContentGPU(docIds, page);
        
        // Add debug logging
        logger.info("Retrieved {} results for current page", results.size());
        
        Map<String, Object> response = new HashMap<>();
        response.put("results", results);
        response.put("totalResults", totalResults);
        response.put("currentPage", page);
        response.put("totalPages", (int) Math.ceil((double) totalResults / 100));
        
        return response;
    }

    private Map<String, Object> createEmptyResponse() {
        Map<String, Object> response = new HashMap<>();
        response.put("results", new ArrayList<>());
        response.put("totalResults", 0);
        response.put("currentPage", 1);
        response.put("totalPages", 0);
        return response;
    }

    private int getLexiconWordId(String word) {
        try {
            logger.info("Loading lexicon from {}", this.lexiconPath);
            ObjectMapper mapper = new ObjectMapper();
            Map<String, Integer> lexicon = mapper.readValue(new File(this.lexiconPath), 
                new TypeReference<Map<String, Integer>>() {});
                
            Integer wordId = lexicon.get(word);
            if (wordId != null) {
                logger.info("Word '{}' found with WordID: {}", word, wordId);
                return wordId;
            } else {
                logger.info("Word '{}' not found in lexicon.", word);
                return 0;
            }
        } catch (FileNotFoundException e) {
            logger.error("Error: Lexicon file '{}' not found.", this.lexiconPath);
            return 0;
        } catch (Exception e) {
            logger.error("Unexpected error while loading lexicon: {}", e.getMessage());
            return 0;
        }
    }

    private String getBarrelPath(int wordId) {
        try {
            logger.info("Loading barrel metadata from {}", this.barrelMetadataPath);
            ObjectMapper mapper = new ObjectMapper();
            Map<String, String> barrelMetadata = mapper.readValue(new File(this.barrelMetadataPath), 
                new TypeReference<Map<String, String>>() {});
    
            // Get number of barrels
            int numBarrels = barrelMetadata.size();
            if (numBarrels == 0) {
                System.out.println("No barrels found in metadata.");
                return "";
            }
    
            // Calculate barrel index (1-based)
            int barrelIndex = (wordId % numBarrels) + 1;
            String barrelKey = String.valueOf(barrelIndex);
    
            String barrelPath = barrelMetadata.get(barrelKey);
            if (barrelPath == null || barrelPath.isEmpty()) {
                System.out.println("No barrel found for index " + barrelKey);
                return "";
            }
    
            System.out.println("Found barrel path: " + barrelPath);
            return barrelPath;
    
        } catch (FileNotFoundException e) {
            System.err.println("Error: Barrel metadata file not found: " + e.getMessage());
            return "";
        } catch (Exception e) {
            System.err.println("Unexpected error accessing barrel metadata: " + e.getMessage());
            return "";
        }
    }


    private List<Integer> getDocIds(String barrelPath, int wordId) {
        try {
            String absolutePath = resolveBarrelPath(barrelPath);
            // logger.info("Loading barrel from {}", absolutePath);
            ObjectMapper mapper = new ObjectMapper();
            Map<String, List<Integer>> barrelData = mapper.readValue(new File(absolutePath),
                new TypeReference<Map<String, List<Integer>>>() {});
    
            List<Integer> docIds = barrelData.getOrDefault(String.valueOf(wordId), new ArrayList<>());
            logger.info("Found {} document IDs for WordID {}", docIds.size(), wordId);
            return docIds;
    
        } catch (Exception e) {
            logger.error("Error reading barrel: {}", e.getMessage());
            return new ArrayList<>();
        }
    }

    // private String identifyDataset(int docId) {
    //     for (Map.Entry<String, int[]> entry : DATASET_RANGES.entrySet()) {
    //         int[] range = entry.getValue();
    //         if (docId >= range[0] && docId <= range[1]) {
    //             return entry.getKey();
    //         }
    //     }
    //     return null;
    // }

    // private Map<String, String> retrieveContent(int docId) {
    //     String datasetName = identifyDataset(docId);
    //     if (datasetName == null) {
    //         logger.error("DocID {} not found in any dataset range", docId);
    //         return null;
    //     }
    
    //     String datasetPath = DATASET_PATHS.get(datasetName);
    //     Map<String, Integer> columnMap = DATASET_COLUMNS.get(datasetName);
        
    //     try (FileReader fileReader = new FileReader(datasetPath);
    //          CSVReader reader = new CSVReaderBuilder(fileReader)
    //             .withSkipLines(1)
    //             .build()) {
                
    //         String[] line;
    //         while ((line = reader.readNext()) != null) {
    //             try {
    //                 String docIdStr = line[0].trim();
    //                 if (!docIdStr.isEmpty() && Integer.parseInt(docIdStr) == docId) {
    //                     Map<String, String> content = new HashMap<>();
    //                     for (Map.Entry<String, Integer> entry : columnMap.entrySet()) {
    //                         int colIndex = entry.getValue();
    //                         if (colIndex < line.length) {
    //                             content.put(entry.getKey(), line[colIndex]);
    //                         }
    //                     }
    //                     return content;
    //                 }
    //             } catch (NumberFormatException e) {
    //                 logger.debug("Skipping invalid line for docId: {}", docId);
    //                 continue;
    //             }
    //         }
    //         return null;
    //     } catch (Exception e) {
    //         logger.error("Error retrieving content for DocID {}: {}", docId, e.getMessage());
    //         return null;
    //     }
    // }

    // private List<SearchResult> getContent(List<Integer> docIds) {
    //     List<SearchResult> results = new ArrayList<>();
    //     for (Integer docId : docIds) {
    //         try {
    //             Map<String, String> content = retrieveContent(docId);
    //             if (content != null) {
    //                 SearchResult result = new SearchResult();
    //                 result.setDocId(docId);
    //                 result.setTitle(content.get("title"));
    //                 result.setDescription(content.get("description"));
    //                 result.setUrl(content.get("url"));
    //                 result.setSource(content.get("source"));
    //                 results.add(result);
    //             }
    //         } catch (Exception e) {
    //             System.err.println("Error retrieving content for DocID " + docId + ": " + e.getMessage());
    //         }
    //     }
    //     return results;
    // }
}
