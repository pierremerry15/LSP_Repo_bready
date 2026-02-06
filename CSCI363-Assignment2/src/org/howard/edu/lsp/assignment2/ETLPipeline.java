package org.howard.edu.lsp.assignment2;

import java.io.*;
import java.math.BigDecimal;
import java.math.RoundingMode;

public class ETLPipeline {

    public static void main(String[] args) {
        File inputFile = new File("data/products.csv");
        File outputFile = new File("data/transformed_products.csv");

        int rowsRead = 0;
        int rowsWritten = 0;
        int rowsSkipped = 0;

        if (!inputFile.exists()) {
            System.out.println("Error: Input file data/products.csv not found.");
            return;
        }

        try (
            BufferedReader reader = new BufferedReader(new FileReader(inputFile));
            BufferedWriter writer = new BufferedWriter(new FileWriter(outputFile))
        ) {
            String header = reader.readLine();
            writer.write("ProductID,Name,Price,Category,PriceRange");
            writer.newLine();

            if (header == null) {
                printSummary(rowsRead, rowsWritten, rowsSkipped, outputFile.getPath());
                return;
            }

            String line;
            while ((line = reader.readLine()) != null) {
                if (line.trim().isEmpty()) {
                    rowsRead++;
                    rowsSkipped++;
                    continue;
                }

                rowsRead++;
                String[] fields = line.split(",");
                if (fields.length != 4) {
                    rowsSkipped++;
                    continue;
                }

                try {
                    int productId = Integer.parseInt(fields[0].trim());
                    String name = fields[1].trim().toUpperCase();
                    BigDecimal price = new BigDecimal(fields[2].trim());
                    String category = fields[3].trim();
                    String originalCategory = category;

                    if (originalCategory.equals("Electronics")) {
                        price = price.multiply(new BigDecimal("0.90"));
                    }

                    price = price.setScale(2, RoundingMode.HALF_UP);

                    if (originalCategory.equals("Electronics") &&
                        price.compareTo(new BigDecimal("500.00")) > 0) {
                        category = "Premium Electronics";
                    }

                    String priceRange;
                    if (price.compareTo(new BigDecimal("10.00")) <= 0) {
                        priceRange = "Low";
                    } else if (price.compareTo(new BigDecimal("100.00")) <= 0) {
                        priceRange = "Medium";
                    } else if (price.compareTo(new BigDecimal("500.00")) <= 0) {
                        priceRange = "High";
                    } else {
                        priceRange = "Premium";
                    }

                    writer.write(
                        productId + "," +
                        name + "," +
                        price.toPlainString() + "," +
                        category + "," +
                        priceRange
                    );
                    writer.newLine();
                    rowsWritten++;

                } catch (Exception e) {
                    rowsSkipped++;
                }
            }

            printSummary(rowsRead, rowsWritten, rowsSkipped, outputFile.getPath());

        } catch (IOException e) {
            System.out.println("Error processing files.");
        }
    }

    private static void printSummary(int read, int written, int skipped, String path) {
        System.out.println("Rows read: " + read);
        System.out.println("Rows transformed: " + written);
        System.out.println("Rows skipped: " + skipped);
        System.out.println("Output written to: " + path);
    }
}
