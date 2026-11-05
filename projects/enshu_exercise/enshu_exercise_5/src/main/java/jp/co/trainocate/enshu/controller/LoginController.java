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
import jp.co.trainocate.enshu.repository.EmpRepository;

@Controller
public class LoginController {
	@Autowired
	private EmpRepository empRepo;

	@GetMapping("/")
	public String showLoginView(EmpForm empForm) {
		return "index";
	}

	@PostMapping("/login")
	public String login(@Valid EmpForm empForm, BindingResult bdResult, HttpSession session) {

		if (bdResult.hasErrors()) {
			return "index";
		}

		Employee emp = empRepo.findByIdAndPassword(empForm.getId(), empForm.getPassword());

		//演習5.3 b. このデータをhtmlで呼び出したいなら、session.user.データ名
		session.setAttribute("user", emp);

		return "redirect:emp/findAll";
	}
}
