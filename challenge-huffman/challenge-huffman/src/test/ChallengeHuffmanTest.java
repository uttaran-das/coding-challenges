package test;

import main.ChallengeHuffman;
import org.junit.jupiter.api.Test;

import java.io.File;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class ChallengeHuffmanTest {
    @Test
    void pdfFileShouldReturnNull() {
        File file = new File("./inputs/test.pdf");
        Map<Character, Integer> frequencyMap = ChallengeHuffman.characterFrequency(file);
        assertNull(frequencyMap);
    }

    @Test
    void frequencyXShouldEqual333andFrequency_t_ShouldEqual223000() {
        File file = new File("./inputs/test.txt");
        Map<Character, Integer> frequencyMap = ChallengeHuffman.characterFrequency(file);
        assertNotEquals(null, frequencyMap);
        assert frequencyMap != null;
        assertEquals(333, frequencyMap.get('X'));
        assertEquals(223000, frequencyMap.get('t'));
    }
}