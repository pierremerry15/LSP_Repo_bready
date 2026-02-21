package org.howard.edu.lsp.assignment3;

public class Main {
    public static void main(String[] args) {
        Extractor extractor = new Extractor("data/products.csv");
        Transformer transformer = new Transformer();
        Loader loader = new Loader("data/transformed_products.csv");

        Pipeline pipeline = new Pipeline(extractor, transformer, loader);

        pipeline.run();

        System.out.println("ETL pipeline executed successfully!");
    }
}