import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.Scanner;

public class login {
    public static void main(String[] args) throws Exception {
        Class.forName("com.mysql.cj.jdbc.Driver");
        Connection con = DriverManager.getConnection("jdbc:mysql://localhost:3306/UserAuthentication", "root",
                "Abhinab@2004");
        Scanner sc = new Scanner(System.in);

        System.out.println("Enter  email");
        // String username = args[0];
        String email = sc.nextLine();

        String queryC = "SELECT COUNT(*) FROM user_database WHERE  email = ?";
        PreparedStatement check = con.prepareStatement(queryC);
        check.setString(1, email);
        ResultSet results = check.executeQuery();
        results.next();

        int userCount = results.getInt(1);
        if (userCount > 0) {
            String queryP = "SELECT password FROM user_database WHERE  email = ?";
            PreparedStatement getPassword = con.prepareStatement(queryP);
            getPassword.setString(1, email);
            ResultSet passwordResult = getPassword.executeQuery();

            if (passwordResult.next()) {
                String password = passwordResult.getString("password");
                System.out.println("Password: " + password);

            }

            else {
                System.out.println("Error");
            }

        }
    }
}
