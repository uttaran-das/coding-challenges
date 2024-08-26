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
        frequencyMap.put('u', 37);
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
        frequencyMap.put('u', 37);
        frequencyMap.put('Z', 2);
        HuffmanNode huffmanTree = HuffmanCoding.buildHuffmanTree(frequencyMap);
        assertNotEquals("100", HuffmanCoding.getHuffmanCode(huffmanTree, 'D'));
    }
}