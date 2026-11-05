package jp.co.trainocate.enshu.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/emp2") //動作確認の際は、localhost:8080/emp2/ で行う
public class EmpController2 {

	/*@Autowired
	private EmployeeService empService;*/
	
	@GetMapping("/")
	public String index() {
		return "/emp2/index";
	}
	//returnの例です。/emp2/xxxに合わせないといけません。
	
	@GetMapping("/showInputView")
	public String showInputView() {
		return "/emp2/emp_input";
	}
	
	//足りないメソッドを追記しましょう。
	
}

