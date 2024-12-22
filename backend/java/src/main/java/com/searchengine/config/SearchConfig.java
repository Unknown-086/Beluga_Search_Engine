package com.searchengine.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import com.fasterxml.jackson.databind.ObjectMapper;

@Configuration
public class SearchConfig {
    @Value("${data.base.path}")
    private String basePath;
    
    @Bean
    public ObjectMapper objectMapper() {
        return new ObjectMapper();
    }
}