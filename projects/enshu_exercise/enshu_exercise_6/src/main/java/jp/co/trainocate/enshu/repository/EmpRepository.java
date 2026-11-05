package jp.co.trainocate.enshu.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import jp.co.trainocate.enshu.entity.Employee;

public interface EmpRepository extends JpaRepository<Employee, Integer>{
	  //演習6.6.c
    //以下の条件で社員情報を取得できるJPQLを記述してください。
    //・エンティティ名はEmployeeとする
    //・salary列が、引数salary以上
    //・location.name列が、引数locationNameと一致
    //・戻り値は、List<Employee>
    //・メソッド名は、findHighSalaryByLocation
    
}
