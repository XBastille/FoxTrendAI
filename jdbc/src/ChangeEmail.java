import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Scanner;
public class ChangeEmail {

	public static void main(String[] args) throws Exception {
		 Scanner sc = new Scanner(System.in);
	     Class.forName("com.mysql.cj.jdbc.Driver");
	     Connection con = getConnection();
	     
	     System.out.println("Enter new email: ");
	     String email = sc.nextLine();
//	     String email = args[0];
	     System.out.println("Enter username: ");
	     String username = sc.nextLine();
//	     String username = args[1];
	     String query = "SELECT COUNT(*) FROM user_database WHERE email = ?";
	     PreparedStatement check = con.prepareStatement(query);
	     check.setString(1, email);
	     ResultSet results = check.executeQuery();
	     results.next();
	     if (results.getInt(1) > 0) 
	       System.out.println("Email exists");
	     else {
	    	 PreparedStatement ps1 = con.prepareStatement("UPDATE user_database SET email = ? WHERE username = ?");
		     ps1.setString(1,email);
		     ps1.setString(2,username);
		     
		     int rows1 = ps1.executeUpdate();
		     
		     if(rows1 > 0) 
		    	 System.out.println("Email Updated!");
		    	
		     else 
			    	 System.out.println("Error");
	     }
		

	}
	
	public static Connection getConnection() throws InterruptedException {
        int retries = 5;
        while (retries > 0) {
            try {
                Connection con = DriverManager.getConnection("jdbc:mysql://localhost:3306/UserAuthentication", "root", "your_password");
                System.out.println("Connected to the database!");
                return con;
            } catch (Exception e) {
                System.out.println("Failed to connect, retrying in 5 seconds...");
                Thread.sleep(5000);
                retries--;
            }
        }
        throw new RuntimeException("Could not connect to the database");
    }

}
