//change hoga yeh

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.Scanner;

public class password {
    public static void main(String[] args) throws Exception {
        Scanner sc = new Scanner(System.in);
        Class.forName("com.mysql.cj.jdbc.Driver");
        Connection con = DriverManager.getConnection("jdbc:mysql://localhost:3306/UserAuthentication", "root",
                "Abhinab@2004");

        String pass = args[0];
        // String pass = sc.nextLine();
        // String cpass = sc.nextLine();

        String query = "SELECT username FROM user_database ORDER BY id DESC LIMIT 1";
        PreparedStatement statement = con.prepareStatement(query);
        ResultSet result = statement.executeQuery();

        if (result.next()) {
            String username = result.getString("username");

            String updateSQL = "UPDATE user_database SET password = ? WHERE username = ?";
            PreparedStatement updateStatement = con.prepareStatement(updateSQL);
            updateStatement.setString(1, pass);
            updateStatement.setString(2, username);

            int rowsUpdated = updateStatement.executeUpdate();
            if (rowsUpdated > 0)

                System.out.println("Password updated successfully for user ");
            else
                System.out.println("No user found with username ");

        } else
            System.out.println("No users found in the database.");

    }

}
