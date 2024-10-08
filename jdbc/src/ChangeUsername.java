import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Scanner;
public class ChangeUsername {

	public static void main(String[] args) throws Exception {
		 Scanner sc = new Scanner(System.in);
	     Class.forName("com.mysql.cj.jdbc.Driver");
	     Connection con = DriverManager.getConnection("jdbc:mysql://localhost:3306/UserAuthentication", "root", "your-password");
	     
	     System.out.println("Enter email: ");
	     String email = sc.nextLine();
//	     String email = args[0];
	     System.out.println("Enter new username: ");
	     String username = sc.nextLine();
//	     String username = args[1];
	     String query = "SELECT COUNT(*) FROM user_database WHERE username = ?";
	     PreparedStatement check = con.prepareStatement(query);
	     check.setString(1, username);
	     ResultSet results = check.executeQuery();
	     results.next();
	     if (results.getInt(1) > 0) 
	       System.out.println("User name exists");
	     else {
	    	 PreparedStatement ps1 = con.prepareStatement("UPDATE user_database SET username = ? WHERE email = ?");
		     ps1.setString(1,username);
		     ps1.setString(2,email);
		     
		     int rows1 = ps1.executeUpdate();
		     
		     if(rows1 > 0) 
		    	 System.out.println("Username Updated!");
		    	
		     else 
			    	 System.out.println("Error");
	     }
	     
	}

}
