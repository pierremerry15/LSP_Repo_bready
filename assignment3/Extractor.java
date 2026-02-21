package org.howard.edu.lsp.assignment3;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

public class Extractor {
    private String sourcePath;

    public Extractor(String sourcePath) {
        this.sourcePath = sourcePath;
    }

    public List<String> extractData() {
        List<String> data = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader(sourcePath))) {
            String line;
            while ((line = br.readLine()) != null) {
                data.add(line);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return data;
    }
}