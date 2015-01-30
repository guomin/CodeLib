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
		List<HotelInfo> hotelList = readHotelInfo("E:/工作/dm/搜索词相关/data1.csv");
		//System.out.println(hotelList.size());
		List<List<Term>> ll=new ArrayList<List<Term>>();
		for (HotelInfo info : hotelList) {
			//System.out.println(info.getName());
			List<Term> tList=NlpAnalysis.parse(info.getName());
			ll.add(tList);
			//System.out.println(tList);
			for (Term term: tList) {
				if(term.getName().length()==1&&(term.getName().equals("店")==false)) {
					System.out.println(tList);
					System.out.println(count++);
					break;
				}
			}
		}
		//writeSeggedHotelName("E:/工作/dm/搜索词相关/rst.txt", ll);
		System.out.println("OK");
		
		String words = "中国是世界四大文明古国之一，有着悠久的历史，距今约5000年前，以中原地区为中心开始出现聚落组织进而成国家和朝代，后历经多次演变和朝代更迭，持续时间较长的朝代有夏、商、周、汉、晋、唐、宋、元、明、清等。中原王朝历史上不断与北方游牧民族交往、征战，众多民族融合成为中华民族。20世纪初辛亥革命后，中国的君主政体退出历史舞台，取而代之的是共和政体。1949年中华人民共和国成立后，在中国大陆建立了人民代表大会制度的政体。中国有着多彩的民俗文化，传统艺术形式有诗词、戏曲、书法和国画等，春节、元宵、清明、端午、中秋、重阳等是中国重要的传统节日。";
		words = "大理念长歌舍";
		words = "大理鸡足山诚美农家乐";
		//Value value = new Value("念长歌舍", "念长", "nt","歌舍","nw");
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
