package jp.co.trainocate.enshu.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;

import jakarta.servlet.http.HttpSession;
import jakarta.validation.Valid;
import jp.co.trainocate.enshu.entity.Employee;
import jp.co.trainocate.enshu.form.EmpForm;
import jp.co.trainocate.enshu.form.EmpForm2;
import jp.co.trainocate.enshu.repository.EmpRepository;

@Controller
public class LoginController {
	@Autowired
	private EmpRepository empRepo;

	@GetMapping("/")
	public String showLoginView() {
		return "index";
	}

	//演習4.1
	@PostMapping("/login")
	public String login(EmpForm empForm) {
		Employee emp = empRepo.findByIdAndPassword(empForm.getId(), empForm.getPassword());

		if (emp == null) {
			return "login_fail";
		}
		return "emp/index";
	}

	//演習4.2

	@GetMapping("/2")
	public String showLoginView2() {
		return "index2";
	}

	@PostMapping("/login2")
	public String loginSession(EmpForm empForm, HttpSession session) {
		Employee emp = empRepo.findByIdAndPassword(empForm.getId(), empForm.getPassword());

		if (emp == null) {
			return "login_fail2";
		}
		session.setAttribute("user", emp);

		return "emp/index";
	}

	//演習4.3

	@GetMapping("/3")
//b. 引数に、Formクラスを入れてください。
	public String showLoginView3(EmpForm2 empForm2) {
		return "index3";
	}
	
	//c. 入力チェックに必要な引数になるように修正してください。
	@PostMapping("/login3")
	public String loginNormal(@Valid EmpForm2 empForm2, BindingResult bdResult, HttpSession session) {

	//d. 入力にエラーがある場合は、ログイン画面へ戻すように条件文を入れてください。
		if (bdResult.hasErrors()) {
			return "index3";
		}

		Employee emp = empRepo.findByIdAndPassword(empForm2.getId(), empForm2.getPassword());

		if (emp == null) { 
			return "index3";
		
		}
		session.setAttribute("user", emp);

		return "emp/index";
	}
}
