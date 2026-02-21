# AI Prompts for Assignment 3

## 1. Prompt: "Can you help me refactor my ETL pipeline to make it more object‑oriented?"
**AI Response**: The AI suggested breaking the pipeline down into smaller, manageable classes: one for reading the file (`Extraction`), one for transforming the data (`Transformation`), and one for writing the output (`Loading`). This would make the code cleaner and easier to maintain.

## 2. Prompt: "How should I handle file reading and writing in an object‑oriented way?"
**AI Response**: The AI recommended putting file reading in the `Extraction` class and file writing in the `Loading` class. This way, each class only deals with one specific thing, which makes the code more organized and reduces the chance of bugs.

## 3. Prompt: "What Java object‑oriented principles should I apply to redesign the pipeline?"
**AI Response**: The AI pointed out the importance of **encapsulation** and **separation of concerns**. Each class should have one job and should not worry about the other parts of the pipeline. This way, the code is more modular and easier to manage.

## 4. Prompt: "Can you give me an example of how to split up the ETL pipeline into classes?"
**AI Response**: The AI provided a simple structure: create an `Extraction` class to handle file reading, a `Transformation` class to modify the data, and a `Loading` class to write the output. It emphasized the idea of giving each class a clear responsibility.

## 5. Prompt: "How can I ensure my redesigned code works the same as the original?"
**AI Response**: The AI suggested comparing the output from the original pipeline with the output from the new one. It also recommended running tests for edge cases like empty files and invalid rows to ensure the new design behaves just as the old one did.