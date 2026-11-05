package jp.co.trainocate.answer.form;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.Data;

@Data
public class UserForm {
	
	@NotNull(message = "社員番号を入力してください")
    private Integer empId;
	
	@NotBlank(message = "パスワードを入力してください")
	@Size(max = 15, message = "15文字以内で入力してください")
    private String password;
	
	@Size(max = 30)
    private String empName;
}
