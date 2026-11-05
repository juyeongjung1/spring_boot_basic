package jp.co.trainocate.enshu.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;

import jp.co.trainocate.enshu.form.BMIForm;

@Controller
public class BMIController {
	
	@GetMapping("/")
	public String index() {
		return "index";
	}
	
	@GetMapping("/2")
	public String index2() {
		return "index2";
	}
	
	@PostMapping("/bmi")
	public String bmi(double height, double weight, Model model) {
		double heightInMeters = height / 100; // 身長をメートル単位に変換
		double bmi = weight / (heightInMeters * heightInMeters);
		model.addAttribute("bmi", bmi);
		return "result";
	}
	
	@PostMapping("/bmi2")
	public String bmi2(BMIForm bmiForm, Model model) {
		double height = bmiForm.getHeight() /100;
		double weight = bmiForm.getWeight();
		double bmi = weight / (height * height);
		bmiForm.setBmi(bmi);
		model.addAttribute("bmiForm", bmiForm);
		
		return "result2";
	}
}
