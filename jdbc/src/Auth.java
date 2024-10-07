import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.Scanner;

public class Auth {
    public static void main(String[] args) throws Exception {
        Scanner sc = new Scanner(System.in);
        Class.forName("com.mysql.cj.jdbc.Driver");
        Connection con = DriverManager.getConnection("jdbc:mysql://db:3306/UserAuthentication", "root", "Abhinab@2004");

        //  String username = sc.nextLine();
           String username = args[0];
        
        String query = "SELECT COUNT(*) FROM user_database WHERE username = ?";
        PreparedStatement statement = con.prepareStatement(query);
        statement.setString(1, username);
        ResultSet result = statement.executeQuery();
        result.next();

        if (result.getInt(1) > 0) {
            System.out.println("Username exists");
        } else {
            System.out.println("Username does not exist");
        }

        result.close();
        statement.close();
        con.close();
        sc.close();
    }
}

