package jp.co.trainocate.enshu.form;

import lombok.Data;

//演習3.5
//c. Formクラスにも、@Dataアノテーションを付けることで、
//Getter&Setterメソッドを自動生成できます。
@Data
public class EmpForm {
	
	private Integer id;
	private String password;
	private String name;
	private Integer salary;
}
