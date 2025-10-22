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
            int searchMethodChosen = scanner.nextInt();

            if (searchMethodChosen == 3)
                break;

            if(searchMethodChosen != 1 && searchMethodChosen != 2){
                System.out.println("invalid number for search method choice entered");
                continue;
            }


            System.out.println("1. Solve with heuristic one");
            System.out.println("2. Solve with heuristic two");
            int heuristicChosen = scanner.nextInt();

            if(heuristicChosen == 1)
                //fill in logic later
                System.out.println("a");
             else if(heuristicChosen == 2)
                 //fill in logic later//
                System.out.println("a");
             else
                System.out.println("invalid number entered");

            if (searchMethodChosen == 1)
                System.out.println("a");
            else
                // call a star later with correct h chosen implementation later
                System.out.println("b");



        }

    }
}