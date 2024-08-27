package main;

import java.io.*;
import java.util.HashMap;
import java.util.Map;

public class ChallengeHuffman {
    public static void main(String[] args) {
        if (args.length == 0) {
            System.out.println("Please provide a filename as a command-line argument.");
            return;
        }
        
        String filename = args[0];
        File file = new File(filename);

        Map<Character, Integer> frequencyMap = characterFrequency(file);

        if(frequencyMap!=null) {
            HuffmanNode huffmanTree = HuffmanCoding.buildHuffmanTree(frequencyMap);
            Map<Character, String> huffmanCodes = HuffmanCoding.getHuffmanCodePrefixTable(huffmanTree);
        }
    }

    public static Map<Character, Integer> characterFrequency(File file) {
        if (!file.exists()) {
            System.out.println("File does not exist.");
            return null;
        }

        if(!isTextFile(file)) {
            System.out.println("The provided file is not a text file.");
            return null;
        }

        try (FileInputStream fis = new FileInputStream(file)) {
            Map<Character, Integer> frequencyMap = new HashMap<>();
            int data;
            while ((data = fis.read()) != -1) {
                char character = (char) data;
                frequencyMap.put(character, frequencyMap.getOrDefault(character, 0) + 1);
            }

            return frequencyMap;
        } catch (IOException e) {
            System.out.println("An error occurred while reading the file: " + e.getMessage());
        }

        return null;
    }

    /*
    The isTextFile method reads the first 512 bytes of the file and checks if they contain any non-printable ASCII
    characters. If they do, the file is considered not a text file.
     */
    private static boolean isTextFile(File file) {
        try (FileInputStream fis = new FileInputStream(file)) {
            byte[] buffer = new byte[512];
            int bytesRead = fis.read(buffer);
            int nonPrintableCount = 0;;
            for (int i = 0; i < bytesRead; i++) {
                /*
                buffer[i] < 0x09:

                    This checks if the byte value is less than 0x09 (which is 9 in decimal, representing the horizontal
                    tab character \t).

                    This includes the null character NUL (0x00) and other control characters before \t.

                (buffer[i] > 0x0D && buffer[i] < 0x20 && buffer[i] != 0x0A):

                    This checks if the byte value is greater than 0x0D (which is 13 in decimal, representing the
                    carriage return character \r) and less than 0x20 (which is 32 in decimal, representing the space
                    character  ).

                    It excludes 0x0A (line feed \n) which are common in text files.

                buffer[i] > 0x7E:

                    This checks if the byte value is greater than 0x7E (which is 126 in decimal, representing the
                    tilde character ~).

                    This excludes characters beyond the standard ASCII printable range.
                 */
                if (buffer[i] < 0x09 || (buffer[i] > 0x0D && buffer[i] < 0x20 && buffer[i] != 0x0A) ||
                        buffer[i] > 0x7E) {
                    nonPrintableCount++;
                }
            }

            // Allowing up to 10% non-printable characters
            double nonPrintableRatio = (double) nonPrintableCount / bytesRead;
            return nonPrintableRatio <= 0.1;
        } catch (IOException e) {
            System.out.println("An error occurred while checking the file: " + e.getMessage());
            return false;
        }
    }
}