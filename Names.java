 

import java.util.ArrayList;

public class Names {

	public static void countWords(String s) {

		String result = "";
		String result1 = "";
		String trimmed = s.trim().replaceAll(" +", " ");
		String[] a = trimmed.split(",");
		ArrayList<Integer> word = new ArrayList<Integer>();
		for (int i = 0; i < a.length; i++) {
			if (word.contains(i)) {
				continue;
			}
			int d = 1;
			for (int j = i + 1; j < a.length; j++) {
				if (a[i].equals(a[j])) {
					d += 1;
					word.add(j);
				}
			}
			result = result + a[i] + ": " + d + ", ";
			result1 = result1 + a[i] + ", ";

		}
		System.out.println("File #1 (Names)");
		System.out.println(result1.substring(0, result1.length() - 2));
		System.out.println();
		System.out.println("File #2 (Name  : Repetitions)");
		System.out.println(result.substring(0, result.length() - 2));
	}

	public static void main(String[] args) {
		countWords("Shyam,Lakshman,Shyam,Shyam,Lakshman");
	}
}
