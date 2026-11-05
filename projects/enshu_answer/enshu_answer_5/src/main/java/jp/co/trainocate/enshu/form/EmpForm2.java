package jp.co.trainocate.enshu.form;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import lombok.Data;

@Data
//登録画面用のFormクラス
public class EmpForm2 {
	
	private Integer id;
	
	@NotBlank(message = "パスワードを入力してください")
	private String password;
	
	@NotBlank(message = "名前を入力してください")
	private String name;
	
	@NotNull(message = "給与を入力してください")
	@Positive(message = "1以上の数値を入力してください")
	private Integer salary;
}
