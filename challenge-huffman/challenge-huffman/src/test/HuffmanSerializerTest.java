package test;

import main.HuffmanCoding;
import main.HuffmanNode;
import main.HuffmanSerializer;
import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class HuffmanSerializerTest {
    @Test
    void serializedStringMatch() {
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
        String expected = "01E001U1D01L01C001Z1K1M";
        String actual = HuffmanSerializer.serializeTree(huffmanTree);
        assertEquals(expected, actual);
    }
}