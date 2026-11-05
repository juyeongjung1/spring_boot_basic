package jp.co.trainocate.enshu.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;

import jp.co.trainocate.enshu.entity.Employee;
import jp.co.trainocate.enshu.entity.Location;
import jp.co.trainocate.enshu.form.EmpForm;
import jp.co.trainocate.enshu.repository.EmpRepository;
import jp.co.trainocate.enshu.repository.LocationRepository;

@Controller
public class EmpController {
	@Autowired
	private EmpRepository empRepo;

	@Autowired
	private LocationRepository locRepo;

	@GetMapping("/")
	public String index() {
		return "index";
	}

	@GetMapping("/2")
	public String index2() {
		return "index2";
	}
	
	@GetMapping("/3")
	public String index3(Model model) {
		List<Employee> list = empRepo.findAll();
		model.addAttribute("empList", list);
		return "emp_list2";
	}
	
	//オプション問題7.6のためのメソッド
	@GetMapping("/4")
	public String ex7_6_index(Model model) {
		List<Employee> list = empRepo.findAll();
		model.addAttribute("empList", list);
		return "emp_list3";
	}
	
	@GetMapping("/showInputView2")
	public String ex7_6_showInputView(Model model) {
		List<Location> list = locRepo.findAll();
		model.addAttribute("locations", list);
		return "emp_input2";

	}
	
	@GetMapping("/findAll")
	public String findAll(Model model) {
		List<Employee> list = empRepo.findAll();
		model.addAttribute("empList", list);
		return "emp_list";
	}

	
	@GetMapping("/showFindById")
	public String showFindById(int id, Model model) {
		Employee emp = empRepo.findById(id).orElse(null);
		model.addAttribute("emp", emp);
		return "emp";
	}

	
	@GetMapping("/showFindByIdSafe")
	public String showFindByIdSafe(int id, Model model) {
		Employee emp = empRepo.findById(id).orElse(null);
		model.addAttribute("emp", emp);
		return "emp2";
	}


	@GetMapping("/showInputView")
	public String showInputView(Model model) {
		List<Location> list = locRepo.findAll();
		model.addAttribute("locations", list);
		return "emp_input";

	}

	@PostMapping("/insertEmp")
	public String insertEmp(EmpForm empForm) {
		Employee emp = new Employee();
		emp.setName(empForm.getName());
		emp.setPassword(empForm.getPassword());
		emp.setSalary(empForm.getSalary());
		emp.setLocationId(empForm.getLocationId());
		
		empRepo.save(emp);

		return "redirect:/findAll";
	}

	@GetMapping("/showSearchForm")
	public String showSearchForm(Model model) {
	    List<Location> list = locRepo.findAll();
	    model.addAttribute("locationList", list);
	    return "emp_search";
	}
	
	@GetMapping("/findHighSalary")
	public String findHighSalary(int salary, String locationName, Model model) {
	    List<Employee> list = empRepo.findHighSalaryByLocation(salary, locationName);
	    model.addAttribute("empList", list);
	    return "emp_list";
	}
	
	
}
