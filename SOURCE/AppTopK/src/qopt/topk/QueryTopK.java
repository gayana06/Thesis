/*
 * Copyright (C) 2011 Clearspring Technologies, Inc. 
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */


package qopt.topk;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import java.util.List;

import com.clearspring.analytics.stream.Counter;
import com.clearspring.analytics.stream.StreamSummary;


public class QueryTopK {

	private static StreamSummary<String> topk = null;
	

    public static void CreateStreamSummary(int capacity)
    {
    	topk=new StreamSummary<String>(capacity);
    }
    
    public static void OfferData(String data)
    {
    	topk.offer(data);
    }
	
    public static String FindTopK()
    {    	
    	return GetSummary(topk);
    }
    
    public static String GetSummary(StreamSummary<String> topk)
    {
    	StringBuilder sb = new StringBuilder();
    	String reply=null;
    	String SEP_COMMA=",";
    	String SEP_PIPE="|";
    	List<Counter<String>> counters = topk.topK(topk.getCapacity());
    	for (Counter<String> counter : counters) 
    	{
    		sb.append(counter.getItem()+SEP_PIPE);
    		sb.append(counter.getCount()+SEP_PIPE);
    		sb.append(counter.getError()+SEP_COMMA);
    	}
    	if (sb.length()>0)
    	{
    		reply=sb.substring(0, sb.length()-1);
    	}
    	return reply;
    }

    public static String formatSummary(StreamSummary<String> topk) {
        StringBuilder sb = new StringBuilder();

        List<Counter<String>> counters = topk.topK(topk.getCapacity());
        String itemHeader = "item";
        String countHeader = "count";
        String errorHeader = "error";

        int maxItemLen = itemHeader.length();
        int maxCountLen = countHeader.length();
        int maxErrorLen = errorHeader.length();

        for (Counter<String> counter : counters) {
            maxItemLen = Math.max(counter.getItem().length(), maxItemLen);
            maxCountLen = Math.max(Long.toString(counter.getCount()).length(), maxCountLen);
            maxErrorLen = Math.max(Long.toString(counter.getError()).length(), maxErrorLen);
        }

        sb.append(String.format("%" + maxItemLen + "s %" + maxCountLen + "s %" + maxErrorLen + "s", itemHeader, countHeader, errorHeader));
        sb.append('\n');
        sb.append(String.format("%" + maxItemLen + "s %" + maxCountLen + "s %" + maxErrorLen + "s", string('-', maxItemLen), string('-', maxCountLen), string('-', maxErrorLen)));
        sb.append('\n');

        for (Counter<String> counter : counters) {
            sb.append(String.format("%" + maxItemLen + "s %" + maxCountLen + "d %" + maxErrorLen + "d", counter.getItem(), counter.getCount(), counter.getError()));
            sb.append('\n');
        }

        return sb.toString();
    }

    public static String string(char c, int len) {
        StringBuilder sb = new StringBuilder(len);
        for (int i = 0; i < len; i++) {
            sb.append(c);
        }
        return sb.toString();
    }
}

