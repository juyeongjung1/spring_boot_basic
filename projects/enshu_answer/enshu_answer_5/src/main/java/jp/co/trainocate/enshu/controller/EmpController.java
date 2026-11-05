package jp.co.trainocate.enshu.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import jakarta.validation.Valid;
import jp.co.trainocate.enshu.entity.Employee;
import jp.co.trainocate.enshu.form.EmpForm2;
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
	public String showInputView(EmpForm2 empForm2) {
		return "emp/emp_input";
	}
	
	@PostMapping("/insertEmp")
	public String insertEmp(@Valid EmpForm2 empForm2, BindingResult bdResult) {
		if (bdResult.hasErrors()) {
			return "emp/emp_input";
		}
		
		Employee emp = new Employee();
		emp.setName(empForm2.getName());
		emp.setPassword(empForm2.getPassword());
		emp.setSalary(empForm2.getSalary());
		empRepo.save(emp);
		
		return "redirect:/emp/findAll";
	}
	
	
	//演習3.6【オプション】
	@GetMapping("/showFindByName")
	public String showFindByName(String name, Model model) {
		System.out.println(name);
		List<Employee> empList = empRepo.findByNameLike("%" + name + "%");
		model.addAttribute("empList", empList);
		System.out.println(empList);
		return "emp/emp_list";
	}
	
	//演習3.7【オプション】
	@GetMapping("/delete/{id}")
	public String deleteEmp(@PathVariable int id) {
		empRepo.deleteById(id);
		return "redirect:/emp/findAll";
	}
}