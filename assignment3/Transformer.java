package org.howard.edu.lsp.assignment3;

import java.util.ArrayList;
import java.util.List;

public class Transformer {

    public List<String> transformData(List<String> data) {
        List<String> transformedData = new ArrayList<>();
        for (String line : data) {
            if (!line.trim().isEmpty()) {
                transformedData.add(line.trim());
            }
        }
        return transformedData;
    }
}