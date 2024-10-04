import java.sql.*;
import java.util.Scanner;

public class finalinput {
	public static void main(String[] args) throws Exception {
		String name = args[0];

		String username = args[1];
		String email = args[2];

		String password = args[3];

		Connection con = DriverManager.getConnection("jdbc:mysql://localhost:3306/UserAuthentication", "root",
				"Abhinab@2004");

		String checkQuery = "SELECT COUNT(*) FROM user_database WHERE username = ?";
		PreparedStatement checkStatement = con.prepareStatement(checkQuery);
		checkStatement.setString(1, username);
		ResultSet resultSet = checkStatement.executeQuery();

		resultSet.next();
		int count = resultSet.getInt(1);

		if (count > 0) {
			System.out.println("Username already exists. Please try a different one.");
		} else {
			String insertQuery = "INSERT INTO user_database (name, username, email, password) VALUES (?, ?, ?, ?)";
			PreparedStatement insertStatement = con.prepareStatement(insertQuery);
			insertStatement.setString(1, name);
			insertStatement.setString(2, username);
			insertStatement.setString(3, email);
			insertStatement.setString(4, password);

			if (insertStatement.executeUpdate() > 0) {
				System.out.println("User registered successfully!");
			}
		}

	}

}
