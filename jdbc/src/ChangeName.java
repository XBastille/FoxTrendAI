import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Scanner;
public class ChangeName {

	public static void main(String[] args) throws Exception {

		 Scanner sc = new Scanner(System.in);
	     Class.forName("com.mysql.cj.jdbc.Driver");
	     Connection con = getConnection();
	     
	     System.out.println("Enter new name: ");
	     String name = sc.nextLine();
//	     String name = args[0];
	     System.out.println("Enter username: ");
	     String username = sc.nextLine();
//	     String username = args[1];
	     
	    	 PreparedStatement ps1 = con.prepareStatement("UPDATE user_database SET name = ? WHERE username = ?");
		     ps1.setString(1,name);
		     ps1.setString(2,username);
		     
		     int rows1 = ps1.executeUpdate();
		     
		     if(rows1 > 0) 
		    	 System.out.println("Name Updated!");
		    	
		     else 
			    	 System.out.println("Error");
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
