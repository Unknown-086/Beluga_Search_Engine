package com.searchengine.controller;

import com.searchengine.service.SearchService;
import com.searchengine.model.SearchResult;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/java")
public class SearchController {
    private final SearchService searchService;

    public SearchController(SearchService searchService) {
        this.searchService = searchService;
    }

    @GetMapping("/search")
    public List<SearchResult> search(@RequestParam String query) {
        return searchService.search(query);
    }
}