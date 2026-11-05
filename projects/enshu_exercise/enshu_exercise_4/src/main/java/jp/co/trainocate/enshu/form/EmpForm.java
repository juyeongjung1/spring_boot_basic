package jp.co.trainocate.enshu.form;

import lombok.Data;

@Data
public class EmpForm {
	
	//演習4.3
	//a.IDとパスワードの入力チェック用アノテーションを付けてください。
	private Integer id;
	private String password;
	private String name;
	private Integer salary;
	
	
}
