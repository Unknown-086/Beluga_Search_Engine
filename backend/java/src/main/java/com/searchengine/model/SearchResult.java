package com.searchengine.model;

public class SearchResult {
    private int docId;
    private String title;
    private String description;
    private String url;
    private String source;
    private Integer numComments; // Optional for Reddit
    private Integer score;       // Optional for Reddit
    private boolean isReddit;    // Flag for Reddit posts

    // Add new getters/setters
    public Integer getNumComments() { return numComments; }
    public void setNumComments(Integer numComments) { this.numComments = numComments; }
    
    public Integer getScore() { return score; }
    public void setScore(Integer score) { this.score = score; }
    
    public boolean getIsReddit() { return isReddit; }
    public void setIsReddit(boolean isReddit) { this.isReddit = isReddit; }
    // Getters and setters
    public int getDocId() { return docId; }
    public void setDocId(int docId) { this.docId = docId; }
    
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    
    public String getUrl() { return url; }
    public void setUrl(String url) { this.url = url; }
    
    public String getSource() { return source; }
    public void setSource(String source) { this.source = source; }
}