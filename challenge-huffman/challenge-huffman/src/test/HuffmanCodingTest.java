package test;

import main.HuffmanCoding;
import main.HuffmanNode;
import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class HuffmanCodingTest {
    @Test
    void zCodeShouldEqual111100() {
        Map<Character, Integer> frequencyMap = new HashMap<>();
        frequencyMap.put('C', 32);
        frequencyMap.put('D', 42);
        frequencyMap.put('E', 120);
        frequencyMap.put('K', 7);
        frequencyMap.put('L', 42);
        frequencyMap.put('M', 24);
        frequencyMap.put('U', 37);
        frequencyMap.put('Z', 2);
        HuffmanNode huffmanTree = HuffmanCoding.buildHuffmanTree(frequencyMap);
        assertEquals("111100", HuffmanCoding.getHuffmanCode(huffmanTree, 'Z'));
    }

    @Test
    void dCodeShouldNotEqual100() {
        Map<Character, Integer> frequencyMap = new HashMap<>();
        frequencyMap.put('C', 32);
        frequencyMap.put('D', 42);
        frequencyMap.put('E', 120);
        frequencyMap.put('K', 7);
        frequencyMap.put('L', 42);
        frequencyMap.put('M', 24);
        frequencyMap.put('U', 37);
        frequencyMap.put('Z', 2);
        HuffmanNode huffmanTree = HuffmanCoding.buildHuffmanTree(frequencyMap);
        assertNotEquals("100", HuffmanCoding.getHuffmanCode(huffmanTree, 'D'));
    }

    @Test
    void huffmanCodePrefixTableTest() {
        Map<Character, Integer> frequencyMap = new HashMap<>();
        frequencyMap.put('C', 32);
        frequencyMap.put('D', 42);
        frequencyMap.put('E', 120);
        frequencyMap.put('K', 7);
        frequencyMap.put('L', 43);
        frequencyMap.put('M', 24);
        frequencyMap.put('U', 37);
        frequencyMap.put('Z', 2);
        HuffmanNode huffmanTree = HuffmanCoding.buildHuffmanTree(frequencyMap);
        Map<Character, String> expectedTable = new HashMap<>();
        expectedTable.put('C', "1110");
        expectedTable.put('D', "101");
        expectedTable.put('E', "0");
        expectedTable.put('K', "111101");
        expectedTable.put('L', "110");
        expectedTable.put('M', "11111");
        expectedTable.put('U', "100");
        expectedTable.put('Z', "111100");
        Map<Character, String> actualTable = HuffmanCoding.getHuffmanCodePrefixTable(huffmanTree);
        assertEquals(expectedTable, actualTable);
    }
}