package jp.co.trainocate.enshu.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import jp.co.trainocate.enshu.entity.Employee;

public interface EmpRepository extends JpaRepository<Employee, Integer>{
	
	//演習6.6-c 正解
	@Query("SELECT e FROM Employee e WHERE e.salary >= :salary AND e.location.name = :locationName")
	List<Employee> findHighSalaryByLocation(int salary, String locationName);

}
