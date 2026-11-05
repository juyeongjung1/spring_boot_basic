package jp.co.trainocate.enshu.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import jp.co.trainocate.enshu.entity.Employee;
import jp.co.trainocate.enshu.form.EmpForm;
import jp.co.trainocate.enshu.service.EmployeeService;

@Controller
@RequestMapping("/emp2")
public class EmpController2 {

	@Autowired
	private EmployeeService empService;
	
	@GetMapping("/")
	public String index() {
		return "index";
	}
	
	@GetMapping("/findAll")
	public String findAll(Model model) {
		List<Employee> empList = empService.findAllEmployees();
		model.addAttribute("empList", empList);
		return "emp_list";
	}
	
	@GetMapping("/findById")
	public String findById(int id, Model model) {
		Employee emp = empService.findEmployeeById(id);
		model.addAttribute("emp", emp);
		return "emp";
	}
	
	
	@GetMapping("/showInputView")
	public String showInputView() {
		return "emp_input";
	}
	
	@PostMapping("/insertEmp")
	public String insertEmp(EmpForm empForm) {
		empService.saveEmployee(empForm);
		return "redirect:/emp2/findAll";
	}
	
	
	@GetMapping("/delete/{id}")
	public String deleteEmp(@PathVariable int id) {
		empService.deleteEmployee(id);
		return "redirect:/emp2/findAll";
	}
}

