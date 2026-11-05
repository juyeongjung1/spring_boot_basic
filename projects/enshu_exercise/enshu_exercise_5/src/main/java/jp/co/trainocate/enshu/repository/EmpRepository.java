package jp.co.trainocate.enshu.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import jp.co.trainocate.enshu.entity.Employee;

public interface EmpRepository extends JpaRepository<Employee, Integer>{
	List<Employee> findBySalary(Integer salary);
	Employee findByIdAndPassword(Integer id, String password);
	
	//演習5 【オプション】
	List<Employee> findByNameLike(String name);
}
