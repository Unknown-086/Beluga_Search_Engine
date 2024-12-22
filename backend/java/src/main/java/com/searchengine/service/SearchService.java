package com.searchengine.service;

import com.searchengine.model.SearchResult;
import org.springframework.stereotype.Service;
import org.json.JSONObject;
import org.json.JSONTokener;
import java.io.*;
import java.nio.file.*;
import java.util.*;

@Service
public class SearchService {
    private static final String BASE_PATH = "../../../../../../../../data/";
    private static final String LEXICON_PATH = BASE_PATH + "Lexicons/SampleTesting/Lexicon_5000.json";
    private static final String BARREL_METADATA_PATH = BASE_PATH + "BarrelData/SampleTesting/PathData/barrel_Hashed_metadata_5000.json";
    
    public List<SearchResult> search(String query) {
        int wordId = getLexiconWordId(query.toLowerCase());
        if (wordId == 0) return new ArrayList<>();
        
        String barrelPath = getBarrelPath(wordId);
        if (barrelPath.isEmpty()) return new ArrayList<>();
        
        List<Integer> docIds = getDocIds(barrelPath, wordId);
        return getContent(docIds);
    }

    private int getLexiconWordId(String word) {
        try {
            System.out.println("Loading lexicon from " + LEXICON_PATH);
            ObjectMapper mapper = new ObjectMapper();
            Map<String, Integer> lexicon = mapper.readValue(new File(LEXICON_PATH), 
                new TypeReference<Map<String, Integer>>() {});
                
            Integer wordId = lexicon.get(word);
            if (wordId != null) {
                System.out.println("Word '" + word + "' found with WordID: " + wordId);
                return wordId;
            } else {
                System.out.println("Word '" + word + "' not found in lexicon.");
                return 0;
            }
        } catch (FileNotFoundException e) {
            System.err.println("Error: Lexicon file '" + LEXICON_PATH + "' not found.");
            return 0;
        } catch (Exception e) {
            System.err.println("Unexpected error while loading lexicon: " + e.getMessage());
            return 0;
        }
    }

    private String getBarrelPath(int wordId) {
        try (FileReader reader = new FileReader(BARREL_METADATA_PATH)) {
            JSONObject metadata = new JSONObject(new JSONTokener(reader));
            return metadata.optString(String.valueOf(wordId), "");
        } catch (IOException e) {
            System.err.println("Error reading barrel metadata: " + e.getMessage());
            return "";
        }
    }

    private List<Integer> getDocIds(String barrelPath, int wordId) {
        try (FileReader reader = new FileReader(barrelPath)) {
            JSONObject barrel = new JSONObject(new JSONTokener(reader));
            JSONArray docIdsArray = barrel.optJSONArray(String.valueOf(wordId));
            
            List<Integer> docIds = new ArrayList<>();
            if (docIdsArray != null) {
                for (int i = 0; i < docIdsArray.length(); i++) {
                    docIds.add(docIdsArray.getInt(i));
                }
            }
            return docIds;
        } catch (IOException e) {
            System.err.println("Error reading barrel: " + e.getMessage());
            return new ArrayList<>();
        }
    }

    private List<SearchResult> getContent(List<Integer> docIds) {
        List<SearchResult> results = new ArrayList<>();
        for (Integer docId : docIds) {
            try {
                // Read from appropriate dataset based on docId range
                SearchResult result = new SearchResult();
                result.setDocId(docId);
                // Set other fields based on dataset content
                results.add(result);
            } catch (Exception e) {
                System.err.println("Error retrieving content for DocID " + docId + ": " + e.getMessage());
            }
        }
        return results;
    }
}