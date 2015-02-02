import java.util.ArrayList;
import java.util.List;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;

import love.cq.domain.Value;
import love.cq.library.Library;

import org.ansj.domain.Term;
import org.ansj.library.UserDefineLibrary;
import org.ansj.splitWord.analysis.NlpAnalysis;
import org.ansj.splitWord.analysis.ToAnalysis;

import sun.security.action.LoadLibraryAction;

class HotelInfo {
	private String name = "";
	private String city = "";
	private float price = 0.0f;

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getCity() {
		return city;
	}

	public void setCity(String city) {
		this.city = city;
	}

	public float getPrice() {
		return price;
	}

	public void setPrice(float price) {
		this.price = price;
	}
}

public class Test {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		int count = 0;
		List<HotelInfo> hotelList = readHotelInfo("E:/����/dm/���������/data1.csv");
		//System.out.println(hotelList.size());
		List<List<Term>> ll=new ArrayList<List<Term>>();
		for (HotelInfo info : hotelList) {
			//System.out.println(info.getName());
			List<Term> tList=NlpAnalysis.parse(info.getName());
			ll.add(tList);
			//System.out.println(tList);
			for (Term term: tList) {
				if(term.getName().length()==1&&(term.getName().equals("��")==false)) {
					System.out.println(tList);
					System.out.println(count++);
					break;
				}
			}
		}
		//writeSeggedHotelName("E:/����/dm/���������/rst.txt", ll);
		System.out.println("OK");
		
		String words = "�й��������Ĵ������Ź�֮һ�������ƾõ���ʷ�����Լ5000��ǰ������ԭ����Ϊ���Ŀ�ʼ���־�����֯�����ɹ��Һͳ���������������ݱ�ͳ�������������ʱ��ϳ��ĳ������ġ��̡��ܡ����������ơ��Ρ�Ԫ��������ȡ���ԭ������ʷ�ϲ����뱱���������彻������ս���ڶ������ںϳ�Ϊ�л����塣20���ͳ������������й��ľ��������˳���ʷ��̨��ȡ����֮���ǹ������塣1949���л����񹲺͹����������й���½����������������ƶȵ����塣�й����Ŷ�ʵ������Ļ�����ͳ������ʽ��ʫ�ʡ�Ϸ�����鷨�͹����ȣ����ڡ�Ԫ�������������硢������������й���Ҫ�Ĵ�ͳ���ա�";
		words = "���������";
		words = "������ɽ����ũ����";
		//Value value = new Value("�����", "�", "nt","����","nw");
        //Library.insertWord(UserDefineLibrary.ambiguityForest, value);
		
		System.out.println(NlpAnalysis.parse(words));

	}
	
	public static void writeSeggedHotelName(String fname, List<List<Term>> list) {
		try {
			File file = new File(fname);
			if(!file.exists()) {
				file.createNewFile();
			}
			OutputStreamWriter writer = new OutputStreamWriter(new FileOutputStream(file), "utf-8");
			BufferedWriter writer2 = new BufferedWriter(writer);
			for (List<Term> listTerm : list) {
				for (Term term: listTerm) {
					writer2.write(term.getName());
					writer2.write("\t");
				}
				writer2.write("\n");
			}
			writer2.close();
		} catch (Exception e) {
			// TODO: handle exception
			e.printStackTrace();
		}
	}

	public static List<HotelInfo> readHotelInfo(String fname) {
		System.out.println("readHotelInfo:\t"+fname);
		List<HotelInfo> retList = new ArrayList<HotelInfo>();
		try {
			File file = new File(fname);
			FileReader freader = new FileReader(file);
			BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(fname), "utf-8"));
			String str = reader.readLine();
			while (str != null) {
				String[] arr = str.split("\t");
				if (arr.length == 3) {
					HotelInfo info = new HotelInfo();
					info.setName(arr[0]);
					info.setCity(arr[2]);
					retList.add(info);
				} else {
					System.out.println("arr.len!=3:\t"+str);
				}
				str = reader.readLine();
			}
		} catch (Exception e) {
			// TODO: handle exception
			e.printStackTrace();
		}
		return retList;
	}

}
