import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;



public class Main {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		try
		{
			int port = Integer.parseInt(args[0]);		
			ServerListen(port);
		}
		catch(Exception ex)
		{
			ex.printStackTrace();
		}
	}
	
	public static void RunBatchFile()
	{
		try
		{
		 ProcessBuilder pb = new ProcessBuilder("/home/ubuntu/myscript.sh", "myArg1", "myArg2");
		 Process p = pb.start();
		 System.out.println("Process started ");
		 BufferedReader reader = new BufferedReader(new InputStreamReader(p.getInputStream()));
		 String line = null;
		 StringBuilder sb=new StringBuilder();
		 while ((line = reader.readLine()) != null)
		 {
		    System.out.println(line);
		    sb.append(line+"\n");
		 }
		 WriteToFile(sb.toString());
		}
		catch(Exception ex)
		{
			System.out.println(ex.getMessage());
		}
	}
	
	private static void ServerListen(int serverport ) throws IOException 
	{
		ServerSocket listener=null;
		
		try
		{
			listener = new ServerSocket(serverport);			
			while (true)
			{
				System.out.println("Server listening on port "+serverport);
				Socket sock=null;
				String dataStream=null;
				try
				{
					sock=listener.accept();
					dataStream=ReadMessage(sock);
					System.out.println("Data stream received = "+dataStream);
					if(dataStream.equals("START"))
						RunBatchFile();
					System.out.println("End of program.");
					
				}
				catch(Exception ex)
				{
					ex.printStackTrace();	
				}
				finally
				{
					sock.close();
				}
			}
		} 
		catch(Exception ex)
		{
			ex.printStackTrace();				
		}
		finally
		{
			listener.close();
		}
	}
	
	private static String ReadMessage(Socket sock) throws IOException 
	{
		BufferedReader input= new BufferedReader(new InputStreamReader(sock.getInputStream()));
		StringBuilder sb=new StringBuilder();
		try
		{
			sb.append(input.readLine());
			
		}
		catch(Exception ex)
		{
			ex.printStackTrace();
		}
		return sb.toString();		
	}
	
	private static void WriteToFile(String content)
	{
		try 
		{
			 
			File file = new File("/home/ubuntu/ssbench-output.txt");
 
			// if file doesnt exists, then create it
			if (file.exists()) {
				file.delete();
				file.createNewFile();
			}
			else
			{
				file.createNewFile();
			}
 
			FileWriter fw = new FileWriter(file.getAbsoluteFile());
			BufferedWriter bw = new BufferedWriter(fw);
			bw.write(content);
			bw.close();
 
			System.out.println("Done");
 
		} 
		catch (IOException e) {
			e.printStackTrace();
		}
	}

}
