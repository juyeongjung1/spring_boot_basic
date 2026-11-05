package jp.co.trainocate.enshu.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;

import jp.co.trainocate.enshu.entity.Employee;
import jp.co.trainocate.enshu.form.EmpForm;
import jp.co.trainocate.enshu.repository.EmpRepository;

@Controller
public class EmpController {
	@Autowired
	private EmpRepository empRepo;

	@GetMapping("/")
	public String index() {
		return "index";
	}

	@GetMapping("/findAll")
	public String findAll(Model model) {
		List<Employee> empList = empRepo.findAll();
		model.addAttribute("empList", empList);
		System.out.println(empList);
		return "emp_list";
	}

	@GetMapping("/showFindById")
	public String showFindById(int id, Model model) {
		Employee emp = empRepo.findById(id).orElse(null);
		model.addAttribute("emp", emp);
		System.out.println(emp);
		return "emp";
	}

	@GetMapping("/showFindBySalary")
	public String showFindBySalary(int salary, Model model) {
		List<Employee> empList = empRepo.findBySalary(salary);
		model.addAttribute("empList", empList);
		System.out.println(empList);
		return "emp_list";
	}
	
	//演習3.5【オプション】
	@GetMapping("/showFindByName")
	public String showFindByName(String name, Model model) {
		System.out.println(name);
		//List<Employee> empList = empRepo.findByNameLike("%" + name + "%");
		List<Employee> empList = empRepo.findByNameContaining(name);
		
		model.addAttribute("empList", empList);
		
		return "emp_list";
	}
	
	@GetMapping("/showInputView")
	public String showInputView() {
		return "emp_input";
	}
	
	@PostMapping("/insertEmp")
	public String insertEmp(EmpForm empForm, Model model) {
		Employee emp = new Employee();
		emp.setName(empForm.getName());
		emp.setPassword(empForm.getPassword());
		emp.setSalary(empForm.getSalary());
		emp = empRepo.save(emp);
		model.addAttribute("emp", emp);
		return "result";
	}
	
	//演習3.7【オプション】
	@GetMapping("/delete/{id}")
	public String deleteEmp(@PathVariable int id) {
		empRepo.deleteById(id);
		return "redirect:/findAll";
	}
}