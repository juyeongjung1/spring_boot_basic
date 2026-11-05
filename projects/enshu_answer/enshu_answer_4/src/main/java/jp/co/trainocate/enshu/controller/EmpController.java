package jp.co.trainocate.enshu.controller;

import java.util.List;

import jakarta.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import jp.co.trainocate.enshu.entity.Employee;
import jp.co.trainocate.enshu.form.EmpForm3;
import jp.co.trainocate.enshu.repository.EmpRepository;

@Controller
@RequestMapping("/emp")
public class EmpController {
	@Autowired
	private EmpRepository empRepo;

	@GetMapping("/")
	public String index() {
		return "emp/index";
	}

	@GetMapping("/findAll")
	public String findAll(Model model) {
		List<Employee> empList = empRepo.findAll();
		model.addAttribute("empList", empList);
		System.out.println(empList);
		return "emp/emp_list";
	}

	@GetMapping("/showFindById")
	public String showFindById(int id, Model model) {
		Employee emp = empRepo.findById(id).orElse(null);
		model.addAttribute("emp", emp);
		System.out.println(emp);
		return "emp/emp";
	}

	@GetMapping("/showFindBySalary")
	public String showFindBySalary(int salary, Model model) {
		List<Employee> empList = empRepo.findBySalary(salary);
		model.addAttribute("empList", empList);
		System.out.println(empList);
		return "emp/emp_list";
	}
	
	@GetMapping("/showInputView")
	public String showInputView(EmpForm3 empForm3) {
		return "emp/emp_input";
	}
	
	@PostMapping("/insertEmp")
	public String insertEmp(@Valid EmpForm3 empForm3, BindingResult bdResult, Model model) {
		if (bdResult.hasErrors()) {
			return "emp/emp_input";
		}
		
		Employee emp = new Employee();
		emp.setName(empForm3.getName());
		emp.setPassword(empForm3.getPassword());
		emp.setSalary(empForm3.getSalary());
		emp = empRepo.save(emp);
		model.addAttribute("emp", emp);
		return "emp/result";
	}
	
	
	@GetMapping("/showFindByName")
	public String showFindByName(String name, Model model) {
		System.out.println(name);
		List<Employee> empList = empRepo.findByNameLike("%" + name + "%");
		model.addAttribute("empList", empList);
		System.out.println(empList);
		return "emp/emp_list";
	}
	
	@GetMapping("/delete/{id}")
	public String deleteEmp(@PathVariable int id) {
		empRepo.deleteById(id);
		return "redirect:/emp/findAll";
	}
}