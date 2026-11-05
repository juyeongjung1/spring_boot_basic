package jp.co.trainocate.enshu.form;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
public class EmpForm {
	
	@NotNull(message = "社員番号を入力してください")
	@Min(value = 1000, message = "4桁以上の社員番号を入力してください")
	private Integer id;
	
	@NotBlank(message = "パスワードを入力してください")
	private String password;
	
	private String name;
	private Integer salary;
}
