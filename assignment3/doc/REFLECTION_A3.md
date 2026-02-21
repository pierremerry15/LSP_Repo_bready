# Reflection on Assignment 2 vs. Assignment 3

## 1. Design Differences
For Assignment 2, I took a procedural approach and put everything in a single class. The main function did it all — reading the file, transforming the data, and writing the output. While this worked, it made the code harder to maintain and test.

For Assignment 3, I shifted to a more **object-oriented** design. Instead of one big block of code, I broke everything down into three separate classes:
- **`Extraction`**: This class takes care of reading the input file, checking for missing files, and skipping over any invalid rows.
- **`Transformation`**: Here, I applied the business logic — like turning product names into uppercase, adjusting prices, and calculating price ranges.
- **`Loading`**: Finally, this class handles writing the transformed data back to a new output file.

This new design allows for better organization and makes the pipeline much easier to extend or modify in the future.

## 2. Object-Oriented Principles Used
- **Encapsulation**: Each class focuses on a specific task, like reading, transforming, or writing, and hides the internal workings from the rest of the program. For example, the logic for reading files is only in the `Extraction` class, and nothing else needs to worry about that.
- **Separation of Concerns**: Splitting the work between `Extraction`, `Transformation`, and `Loading` makes each class much more focused on what it needs to do. This helps in debugging, maintenance, and also makes the code more understandable.
- **Reusability**: The classes are self-contained, which means I can reuse them for future pipelines or extend them if I need new functionality.

## 3. How It Works the Same
Even though the design is different, the functionality remains the same. The pipeline still:
- Reads the input data (`data/products.csv`).
- Applies the same transformation logic.
- Outputs the transformed data to the same file (`data/transformed_products.csv`).

I ran several tests using the same input data and compared the output. Everything works just as before — I made sure the output was exactly the same, including handling edge cases like missing files and invalid rows.

## 4. Final Thoughts
At the end of the day, the biggest change is how much more **maintainable** and **scalable** the program is now. The modular design makes it easier to update, extend, and troubleshoot, while still keeping the exact functionality from Assignment 2.