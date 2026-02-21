package org.howard.edu.lsp.assignment3;

import java.io.*;
import java.util.List;

public class Loader {
    private String destinationPath;

    public Loader(String destinationPath) {
        this.destinationPath = destinationPath;
    }

    public void loadData(List<String> data) {
        try (BufferedWriter bw = new BufferedWriter(new FileWriter(destinationPath))) {
            for (String line : data) {
                bw.write(line);
                bw.newLine();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}