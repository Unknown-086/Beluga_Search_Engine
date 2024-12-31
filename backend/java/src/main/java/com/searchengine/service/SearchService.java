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
import java.util.stream.Collectors;


@Service
public class SearchService {
    private static final Logger logger = LoggerFactory.getLogger(SearchService.class);
    private final GPUContentRetriever gpuContentRetriever;
    private final String basePath;
    private final String lexiconPath;
    private final String barrelMetadataPath;

        // Add cache fields
    private Map<String, Integer> lexiconCache;
    private Map<String, String> barrelMetadataCache;
    
    
        // Add cache initialization
    @PostConstruct
    private void initCache() {
        logger.info("Initializing caches...");
        lexiconCache = loadLexicon();
        barrelMetadataCache = loadBarrelMetadata();
        logger.info("Caches initialized");
    }

    // Add cache loading methods
    private Map<String, Integer> loadLexicon() {
        try {
            ObjectMapper mapper = new ObjectMapper();
            return mapper.readValue(new File(lexiconPath), new TypeReference<Map<String, Integer>>() {});
        } catch (Exception e) {
            logger.error("Error loading lexicon: {}", e.getMessage());
            return new HashMap<>();
        }
    }
    
    private Map<String, String> loadBarrelMetadata() {
        try {
            ObjectMapper mapper = new ObjectMapper();
            return mapper.readValue(new File(barrelMetadataPath), new TypeReference<Map<String, String>>() {});
        } catch (Exception e) {
            logger.error("Error loading barrel metadata: {}", e.getMessage());
            return new HashMap<>();
        }
    }

            // Add cache lookup methods
    private int getLexiconWordIdFromCache(String word) {
        return lexiconCache.getOrDefault(word.toLowerCase(), 0);
    }

    private String getBarrelPathFromCache(int wordId) {
        int barrelId = wordId % 4000 + 1;
        String barrelKey = String.valueOf(barrelId);
        return barrelMetadataCache.getOrDefault(barrelKey, "");
    }

    

    public SearchService(GPUContentRetriever gpuContentRetriever) {
        this.gpuContentRetriever = gpuContentRetriever;
        
        File projectDir = new File(System.getProperty("user.dir"))
            .getParentFile()
            .getParentFile();
        
        this.basePath = new File(projectDir, "data").getAbsolutePath();
        this.lexiconPath = new File(basePath, "Lexicons/Testing/Lexicon_Testing_User.json").getAbsolutePath();
        this.barrelMetadataPath = new File(basePath, "BarrelData/Testing/PathData/Barrels_Testing_Metadata.json").getAbsolutePath();
        
        createDirectoriesIfNeeded();
        verifyPaths();
    }
   
    
    
    private void createDirectoriesIfNeeded() {
        new File(lexiconPath).getParentFile().mkdirs();
        new File(barrelMetadataPath).getParentFile().mkdirs();
    }

    private void verifyPaths() {
        if (!new File(lexiconPath).exists()) {
            throw new RuntimeException("Lexicon file not found: " + lexiconPath);
        }
        if (!new File(barrelMetadataPath).exists()) {
            throw new RuntimeException("Barrel metadata file not found: " + barrelMetadataPath);
        }
    }

    public Map<String, Object> search(String query, int page, String source) {
        List<String> queryWords = Arrays.asList(query.split(","));
        return search(queryWords, page, source);
    }
    
    public Map<String, Object> search(List<String> queryWords, int page, String source) {
        if (queryWords == null || queryWords.isEmpty()) {
            return createEmptyResponse();
        }
    
        if (queryWords.size() == 1) {
            return searchSingleWord(queryWords.get(0), page, source);
        }
    
        return searchMultiWord(queryWords, page, source);
    }
    
    public Map<String, Object> searchSingleWord(String query, int page, String source) {
        logger.info("Starting search for query: {} page: {} source: {}", query, page, source);
        
        int wordId = getLexiconWordIdFromCache(query);
        if (wordId == 0) {
            logger.info("No word ID found for query: {}", query);
            return createEmptyResponse();
        }
        
        String barrelPath = getBarrelPathFromCache(wordId);
        if (barrelPath.isEmpty()) {
            logger.info("No barrel path found for word ID: {}", wordId);
            return createEmptyResponse();
        }
        
        Map<String, Double> rankedDocs = getDocIdsWithRanks(barrelPath, wordId);
        List<Integer> docIds = rankedDocs.entrySet().stream()
            .sorted(Map.Entry.<String, Double>comparingByValue().reversed())
            .map(e -> Integer.parseInt(e.getKey()))
            .collect(Collectors.toList());
            
        List<Object> contentResult = gpuContentRetriever.getContentGPU(docIds, page, source);
        return createResponse(contentResult, page);
    }

    private Map<String, Object> searchMultiWord(List<String> words, int page, String source) {
        try {
            long startTime = System.currentTimeMillis();
            
            // Get docIds and ranks for each word
            Map<String, Map<String, Double>> wordDocuments = new HashMap<>();
            for (String word : words) {
                int wordId = getLexiconWordIdFromCache(word);
                if (wordId == 0) continue;
                
                String barrelPath = getBarrelPathFromCache(wordId);
                if (barrelPath.isEmpty()) continue;
                
                Map<String, Double> docRanks = getDocIdsWithRanks(barrelPath, wordId);
                wordDocuments.put(word, docRanks);
            }
    
            if (wordDocuments.isEmpty()) {
                return createEmptyResponse();
            }
    
            // Group by intersection levels
            Map<Integer, Map<String, Double>> intersectionLevels = groupByIntersection(wordDocuments);
            
            // Get max intersection level (number of words that matched)
            int maxLevel = words.size();
            
            // Combine and sort results by intersection level and rank
            List<Integer> finalDocIds = combineAndSortResults(intersectionLevels, maxLevel);
    
            logger.info("Results processed in {}ms", System.currentTimeMillis() - startTime);
                
            List<Object> contentResult = gpuContentRetriever.getContentGPU(finalDocIds, page, source);
            return createResponse(contentResult, page);
    
        } catch (Exception e) {
            logger.error("Error in multi-word search: {}", e.getMessage());
            return createEmptyResponse();
        }
    }
    
    private Map<Integer, Map<String, Double>> groupByIntersection(Map<String, Map<String, Double>> wordDocuments) {
        Map<Integer, Map<String, Double>> intersectionLevels = new HashMap<>();
        
        // Get all unique docIds
        Set<String> allDocIds = wordDocuments.values().stream()
                .flatMap(m -> m.keySet().stream())
                .collect(Collectors.toSet());
    
        for (String docId : allDocIds) {
            int intersectionCount = 0;
            double totalRank = 0.0;
            
            // Count document appearances and sum ranks
            for (Map<String, Double> wordDocs : wordDocuments.values()) {
                if (wordDocs.containsKey(docId)) {
                    intersectionCount++;
                    totalRank += wordDocs.get(docId);
                }
            }
            
            // Group by intersection count
            intersectionLevels.computeIfAbsent(intersectionCount, k -> new HashMap<>())
                    .put(docId, totalRank);
        }
        return intersectionLevels;
    }
    
    private List<Integer> combineAndSortResults(Map<Integer, Map<String, Double>> intersectionLevels, int maxLevel) {
        List<String> orderedDocIds = new ArrayList<>();
        
        // Process from highest to lowest intersection level
        for (int level = maxLevel; level > 0; level--) {
            Map<String, Double> docsAtLevel = intersectionLevels.get(level);
            if (docsAtLevel != null) {
                // Sort docs at this level by rank
                List<String> sortedDocs = docsAtLevel.entrySet().stream()
                        .sorted(Map.Entry.<String, Double>comparingByValue().reversed())
                        .map(Map.Entry::getKey)
                        .collect(Collectors.toList());
                orderedDocIds.addAll(sortedDocs);
            }
        }
        
        // Convert to integers for final result
        return orderedDocIds.stream()
                .map(Integer::parseInt)
                .collect(Collectors.toList());
    }


    private Map<String, Double> getDocIdsWithRanks(String barrelPath, int wordId) {
        try {
            ObjectMapper mapper = new ObjectMapper();
            Map<String, Map<String, Double>> barrelData = mapper.readValue(
                new File(barrelPath),
                new TypeReference<Map<String, Map<String, Double>>>() {}
            );
            
            return barrelData.getOrDefault(String.valueOf(wordId), new HashMap<>());
        } catch (Exception e) {
            logger.error("Error reading barrel: {}", e.getMessage());
            return new HashMap<>();
        }
    }
    
    private Map<String, Object> createResponse(List<Object> contentResult, int page) {
        List<SearchResult> results = (List<SearchResult>) contentResult.get(0);
        int totalResults = (Integer) contentResult.get(1);
    
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
}
