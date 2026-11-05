package jp.co.trainocate.answer.form;

import lombok.Data;

@Data
public class UserForm {
	
    
//入力値がない場合、"社員番号を入力してください"のエラーを表示するアノテーションを付けてください
    private Integer empId;
    
  //入力値がない場合、"パスワードを入力してください"のエラーを表示するアノテーションを付けてください    
  //15文字を超える場合、"15文字以内で入力してください"のエラーを表示するアノテーションを付けてください    
    private String password;
    private String empName;
}
