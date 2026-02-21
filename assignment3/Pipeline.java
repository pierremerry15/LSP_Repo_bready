package org.howard.edu.lsp.assignment3;

import java.util.List;

public class Pipeline {
    private Extractor extractor;
    private Transformer transformer;
    private Loader loader;

    public Pipeline(Extractor extractor, Transformer transformer, Loader loader) {
        this.extractor = extractor;
        this.transformer = transformer;
        this.loader = loader;
    }

    public void run() {
        List<String> extractedData = extractor.extractData();
        List<String> transformedData = transformer.transformData(extractedData);
        loader.loadData(transformedData);
    }
}