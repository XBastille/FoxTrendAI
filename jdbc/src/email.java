import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.Scanner;

public class email {
    public static void main(String[] args) throws Exception {
        Scanner sc = new Scanner(System.in);
        Class.forName("com.mysql.cj.jdbc.Driver");
        Connection con = DriverManager.getConnection("jdbc:mysql://localhost:3306/UserAuthentication", "root", "Abhinab@2004");

        // String email = sc.nextLine();
         String email = args[0];
        
        String query = "SELECT COUNT(*) FROM user_database WHERE email = ?";
        PreparedStatement statement = con.prepareStatement(query);
        statement.setString(1, email);
        ResultSet result = statement.executeQuery();
        result.next();

        if (result.getInt(1) > 0) {
            System.out.println("Email exists");
        } else {
            System.out.println("Email does not exists");
        }

        result.close();
        statement.close();
        con.close();
        sc.close();
    }
}
