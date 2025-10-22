import java.util.Scanner;

public class Main {

    public static void main(String[] args) {

        TilePuzzle tilePuzzle = new TilePuzzle();
        Scanner scanner = new Scanner(System.in);

        int[][] start = {
                {1, 4, 3},
                {2, 5, 6},
                {7, 8, 0}
        };


        while (true) {
            System.out.println("1.solve with greedy best first search method");
            System.out.println("2.solve with A* Search method");
            System.out.println("3.exit");
            String choice = scanner.next();

            if (choice.equals("3"))
                break;

            System.out.println("1. Solve with heuristic one");
            System.out.println("2. Solve with heuristic two");
            String h_choice = scanner.next();
            if(h_choice.equals("1"))
                //fill in logic later
                continue;
             else if(h_choice.equals("2"))
                 //fill in logic later//
                 continue;
             else
                System.out.println("invalid choice entered");
                 continue;

            if(choice.equals("1"))
                //greedy later with correct h chosen
                continue;
            else if(h_choice.equals("2"))
                //a star later with correct h chosen
                continue;
            else {
                System.out.println("invalid choice entered");
                continue;
            }



        }

    }
}