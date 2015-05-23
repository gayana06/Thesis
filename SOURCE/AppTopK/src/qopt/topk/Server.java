package qopt.topk;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintStream;
import java.net.ServerSocket;
import java.net.Socket;

public class Server {

	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		try
		{
			int port = Integer.parseInt(args[0]);
			int k=Integer.parseInt(args[1]);			
			ServerListen(port,k);
		}
		catch(Exception ex)
		{
			ex.printStackTrace();
		}
	}
	
	private static void ServerListen(int serverport,int k ) throws IOException 
	{
		ServerSocket listener=null;
		
		try
		{
			listener = new ServerSocket(serverport);
			System.out.println("Server listening on port "+serverport);
			while (true)
			{
				Socket sock=null;
				String dataStream=null;
				try
				{
					sock=listener.accept();
					QueryTopK.CreateStreamSummary(k);
					dataStream=ReadMessage(sock);
					System.out.println("Data stream received = "+dataStream);
					String response=ProcessStream(dataStream);
					SendResponse(sock, response);					
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
	
	private static String ProcessStream(String dataStream)
	{
		String sep_pipe="\\|";
		String[] datalist=dataStream.split(sep_pipe);
		String result=null;
		if(datalist.length>0)
		{
			for (String data : datalist) 
			{
				QueryTopK.OfferData(data);
			}
			result=QueryTopK.FindTopK();
		}
		return result;
		
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
	
	private  static void SendResponse(Socket sock,String response) throws IOException 
	{
		BufferedWriter output = new BufferedWriter(new OutputStreamWriter(sock.getOutputStream()));
		try
		{
			output.write(response);
			output.flush();
		}
		catch(Exception ex)
		{
			ex.printStackTrace();
		}
	}
}
