# personas/bias_detection.py
"""
Bias Detection and Mitigation Framework
Implements academic research-based bias detection for synthetic personas
"""

import json
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import pandas as pd
from collections import Counter, defaultdict
import random


@dataclass
class BiasAlert:
    """Bias detection alert"""
    bias_type: str
    severity: str  # 'low', 'medium', 'high', 'critical'
    description: str
    affected_personas: List[str]
    mitigation_suggestions: List[str]
    detected_at: str = None
    
    def __post_init__(self):
        if self.detected_at is None:
            self.detected_at = datetime.now().isoformat()


class StereotypeDetector:
    """Detect stereotypical patterns in persona generation"""
    
    def __init__(self):
        # Define known stereotypical correlations to avoid
        self.problematic_correlations = {
            "age_income": {
                "description": "Young people always having low income",
                "pattern": lambda p: p.get("age", 30) < 25 and "Alto" in str(p.get("income_bracket", ""))
            },
            "gender_tech": {
                "description": "Gender-based technology adoption assumptions",
                "pattern": lambda p: p.get("gender") == "Femenino" and p.get("technology_adoption") in ["Innovador", "Early adopter"]
            },
            "education_service": {
                "description": "Education level determining service type",
                "pattern": lambda p: p.get("education_level") == "Primaria" and p.get("service_type") == "Postpago"
            },
            "rural_tech": {
                "description": "Rural users with high tech adoption",
                "pattern": lambda p: p.get("geographic_region") == "Rural" and p.get("technology_adoption") == "Innovador"
            },
            "age_brand": {
                "description": "Age-based brand preferences",
                "pattern": lambda p: p.get("age", 30) > 60 and p.get("current_operator") == "Tigo"
            }
        }
        
        # Positive stereotypes to detect (also problematic)
        self.positive_stereotypes = {
            "perfect_millennial": "Millennials always tech-savvy and high-earning",
            "ideal_urban_user": "Urban users always satisfied and high-spending",
            "educated_loyalist": "Educated users always brand loyal"
        }
        
        # Protected characteristics requiring special attention
        self.protected_characteristics = [
            "gender", "age", "education_level", "income_bracket", 
            "geographic_region", "religious_spirituality", "marital_status"
        ]
    
    def detect_stereotypes_in_batch(self, personas: List[Dict[str, Any]]) -> List[BiasAlert]:
        """Detect stereotypical patterns in a batch of personas"""
        alerts = []
        
        # Check for problematic correlations
        for correlation_id, correlation_def in self.problematic_correlations.items():
            matching_personas = []
            
            for persona in personas:
                characteristics = persona.get("characteristics", {})
                if correlation_def["pattern"](characteristics):
                    matching_personas.append(persona["id"])
            
            # Calculate percentage
            match_rate = len(matching_personas) / len(personas) if personas else 0
            
            if match_rate > 0.7:  # More than 70% following stereotype
                severity = "high" if match_rate > 0.9 else "medium"
                alerts.append(BiasAlert(
                    bias_type="stereotype_correlation",
                    severity=severity,
                    description=f"High correlation detected: {correlation_def['description']} ({match_rate:.1%})",
                    affected_personas=matching_personas,
                    mitigation_suggestions=[
                        "Generate more counter-stereotypical examples",
                        "Review correlation logic in generation",
                        "Increase diversity in affected characteristics"
                    ]
                ))
        
        # Check for lack of diversity in protected characteristics
        diversity_alerts = self._check_diversity_in_protected_characteristics(personas)
        alerts.extend(diversity_alerts)
        
        # Check for positive stereotype clustering
        positive_alerts = self._detect_positive_stereotypes(personas)
        alerts.extend(positive_alerts)
        
        return alerts
    
    def _check_diversity_in_protected_characteristics(self, personas: List[Dict[str, Any]]) -> List[BiasAlert]:
        """Check diversity in protected characteristics"""
        alerts = []
        
        for characteristic in self.protected_characteristics:
            values = []
            for persona in personas:
                value = persona.get("characteristics", {}).get(characteristic)
                if value is not None:
                    values.append(str(value))
            
            if not values:
                continue
            
            # Calculate diversity score
            value_counts = Counter(values)
            total_count = len(values)
            
            # Check if one value dominates (>70%)
            max_percentage = max(value_counts.values()) / total_count
            
            if max_percentage > 0.7:
                dominant_value = max(value_counts, key=value_counts.get)
                
                alerts.append(BiasAlert(
                    bias_type="lack_of_diversity",
                    severity="medium" if max_percentage > 0.8 else "low",
                    description=f"Low diversity in {characteristic}: {dominant_value} represents {max_percentage:.1%}",
                    affected_personas=[p["id"] for p in personas 
                                     if str(p.get("characteristics", {}).get(characteristic)) == dominant_value],
                    mitigation_suggestions=[
                        f"Increase diversity in {characteristic}",
                        "Apply stratified sampling",
                        "Review generation weights for this characteristic"
                    ]
                ))
        
        return alerts
    
    def _detect_positive_stereotypes(self, personas: List[Dict[str, Any]]) -> List[BiasAlert]:
        """Detect unrealistically positive stereotype clustering"""
        alerts = []
        
        # Check for "perfect personas" - unrealistically positive on all dimensions
        perfect_personas = []
        
        for persona in personas:
            characteristics = persona.get("characteristics", {})
            
            # Count positive indicators
            positive_indicators = 0
            total_indicators = 0
            
            # High satisfaction indicators
            if characteristics.get("brand_perception_tigo") in ["Muy positiva", "Positiva"]:
                positive_indicators += 1
            total_indicators += 1
            
            if characteristics.get("customer_service_experience") in ["Excelente", "Buena"]:
                positive_indicators += 1
            total_indicators += 1
            
            if characteristics.get("recommendation_likelihood", 0) > 8:
                positive_indicators += 1
            total_indicators += 1
            
            if characteristics.get("operator_loyalty", 0) > 8:
                positive_indicators += 1
            total_indicators += 1
            
            # If too many positive indicators
            positive_rate = positive_indicators / total_indicators if total_indicators > 0 else 0
            if positive_rate > 0.8:  # More than 80% positive
                perfect_personas.append(persona["id"])
        
        if len(perfect_personas) > len(personas) * 0.3:  # More than 30% "perfect"
            alerts.append(BiasAlert(
                bias_type="positive_stereotype",
                severity="medium",
                description=f"Too many unrealistically positive personas ({len(perfect_personas)}/{len(personas)})",
                affected_personas=perfect_personas,
                mitigation_suggestions=[
                    "Add more realistic mixed experiences",
                    "Include personas with legitimate complaints",
                    "Balance positive and negative characteristics"
                ]
            ))
        
        return alerts


class DemographicValidator:
    """Validate personas against real demographic data"""
    
    def __init__(self, honduras_demographics: Dict[str, Any]):
        self.honduras_demographics = honduras_demographics
        self.tolerance_threshold = 0.15  # 15% tolerance from expected distribution
    
    def validate_demographic_distribution(self, personas: List[Dict[str, Any]]) -> List[BiasAlert]:
        """Validate that persona demographics match expected distributions"""
        alerts = []
        
        # Validate age distribution
        age_alerts = self._validate_age_distribution(personas)
        alerts.extend(age_alerts)
        
        # Validate gender distribution
        gender_alerts = self._validate_gender_distribution(personas)
        alerts.extend(gender_alerts)
        
        # Validate income distribution
        income_alerts = self._validate_income_distribution(personas)
        alerts.extend(income_alerts)
        
        # Validate geographic distribution
        geo_alerts = self._validate_geographic_distribution(personas)
        alerts.extend(geo_alerts)
        
        return alerts
    
    def _validate_age_distribution(self, personas: List[Dict[str, Any]]) -> List[BiasAlert]:
        """Validate age distribution against Honduras demographics"""
        alerts = []
        
        # Get age groups from personas
        age_groups = defaultdict(int)
        total_personas = len(personas)
        
        for persona in personas:
            age = persona.get("characteristics", {}).get("age", 30)
            age_group = self._get_age_group(age)
            age_groups[age_group] += 1
        
        # Compare with expected distribution
        expected = self.honduras_demographics.get("age_distribution", {})
        
        for age_group, expected_percentage in expected.items():
            actual_count = age_groups.get(age_group, 0)
            actual_percentage = actual_count / total_personas if total_personas > 0 else 0
            
            difference = abs(actual_percentage - expected_percentage)
            
            if difference > self.tolerance_threshold:
                severity = "high" if difference > 0.25 else "medium"
                
                alerts.append(BiasAlert(
                    bias_type="demographic_mismatch",
                    severity=severity,
                    description=f"Age group {age_group}: {actual_percentage:.1%} vs expected {expected_percentage:.1%}",
                    affected_personas=[],
                    mitigation_suggestions=[
                        f"Adjust age generation to match Honduras demographics",
                        f"Target {expected_percentage:.1%} for {age_group} group"
                    ]
                ))
        
        return alerts
    
    def _validate_gender_distribution(self, personas: List[Dict[str, Any]]) -> List[BiasAlert]:
        """Validate gender distribution"""
        alerts = []
        
        gender_counts = defaultdict(int)
        total_personas = len(personas)
        
        for persona in personas:
            gender = persona.get("characteristics", {}).get("gender", "")
            if gender:
                gender_counts[gender] += 1
        
        expected = self.honduras_demographics.get("gender_distribution", {})
        
        for gender, expected_percentage in expected.items():
            actual_count = gender_counts.get(gender, 0)
            actual_percentage = actual_count / total_personas if total_personas > 0 else 0
            
            difference = abs(actual_percentage - expected_percentage)
            
            if difference > self.tolerance_threshold:
                alerts.append(BiasAlert(
                    bias_type="demographic_mismatch",
                    severity="medium",
                    description=f"Gender {gender}: {actual_percentage:.1%} vs expected {expected_percentage:.1%}",
                    affected_personas=[],
                    mitigation_suggestions=[
                        "Balance gender distribution",
                        f"Target {expected_percentage:.1%} for {gender}"
                    ]
                ))
        
        return alerts
    
    def _validate_income_distribution(self, personas: List[Dict[str, Any]]) -> List[BiasAlert]:
        """Validate income distribution"""
        alerts = []
        
        income_counts = defaultdict(int)
        total_personas = len(personas)
        
        for persona in personas:
            income = persona.get("characteristics", {}).get("income_bracket", "")
            if income:
                income_counts[income] += 1
        
        expected = self.honduras_demographics.get("income_distribution", {})
        
        for income_bracket, expected_percentage in expected.items():
            actual_count = income_counts.get(income_bracket, 0)
            actual_percentage = actual_count / total_personas if total_personas > 0 else 0
            
            difference = abs(actual_percentage - expected_percentage)
            
            if difference > self.tolerance_threshold:
                severity = "high" if "Alto" in income_bracket and difference > 0.1 else "medium"
                
                alerts.append(BiasAlert(
                    bias_type="demographic_mismatch", 
                    severity=severity,
                    description=f"Income {income_bracket}: {actual_percentage:.1%} vs expected {expected_percentage:.1%}",
                    affected_personas=[],
                    mitigation_suggestions=[
                        "Adjust income distribution to match Honduras reality",
                        f"Target {expected_percentage:.1%} for {income_bracket}"
                    ]
                ))
        
        return alerts
    
    def _validate_geographic_distribution(self, personas: List[Dict[str, Any]]) -> List[BiasAlert]:
        """Validate geographic distribution"""
        alerts = []
        
        geo_counts = defaultdict(int)
        total_personas = len(personas)
        
        for persona in personas:
            region = persona.get("characteristics", {}).get("geographic_region", "")
            if region:
                geo_counts[region] += 1
        
        expected = self.honduras_demographics.get("geographic_distribution", {})
        
        for region, expected_percentage in expected.items():
            actual_count = geo_counts.get(region, 0)
            actual_percentage = actual_count / total_personas if total_personas > 0 else 0
            
            difference = abs(actual_percentage - expected_percentage)
            
            if difference > self.tolerance_threshold:
                alerts.append(BiasAlert(
                    bias_type="demographic_mismatch",
                    severity="medium",
                    description=f"Region {region}: {actual_percentage:.1%} vs expected {expected_percentage:.1%}",
                    affected_personas=[],
                    mitigation_suggestions=[
                        "Balance geographic distribution",
                        f"Target {expected_percentage:.1%} for {region}"
                    ]
                ))
        
        return alerts
    
    def _get_age_group(self, age: int) -> str:
        """Convert age to age group"""
        if age <= 25:
            return "18-25"
        elif age <= 35:
            return "26-35"
        elif age <= 50:
            return "36-50"
        elif age <= 65:
            return "51-65"
        else:
            return "65+"


class SycophancyDetector:
    """Detect artificial agreeableness and sycophantic patterns"""
    
    def __init__(self):
        # Sycophancy indicators
        self.sycophancy_patterns = {
            "excessive_positivity": [
                "siempre excelente", "todo perfecto", "nunca problemas",
                "completamente satisfecho", "sin quejas"
            ],
            "lack_of_criticism": [
                "no criticism detected", "only positive responses",
                "agrees with everything"
            ],
            "generic_responses": [
                "en general bien", "todo normal", "como siempre",
                "sin comentarios específicos"
            ]
        }
        
        # Authentic response indicators
        self.authentic_indicators = [
            "specific_complaints", "balanced_perspectives", 
            "personal_experiences", "conditional_satisfaction"
        ]
    
    def detect_sycophancy_in_batch(self, personas: List[Dict[str, Any]], 
                                 responses: List[str] = None) -> List[BiasAlert]:
        """Detect sycophantic patterns in persona batch"""
        alerts = []
        
        # Check persona characteristics for sycophancy risk
        high_agreeableness_count = 0
        low_criticism_count = 0
        
        for persona in personas:
            characteristics = persona.get("characteristics", {})
            
            # Check for unrealistically high agreeableness
            agreeableness = characteristics.get("personality_agreeableness", 5)
            if agreeableness > 8:
                high_agreeableness_count += 1
            
            # Check for lack of negative experiences
            service_exp = characteristics.get("customer_service_experience", "Regular")
            brand_perception = characteristics.get("brand_perception_tigo", "Neutral")
            
            if service_exp in ["Excelente", "Buena"] and brand_perception in ["Muy positiva", "Positiva"]:
                low_criticism_count += 1
        
        # Generate alerts based on patterns
        total_personas = len(personas)
        
        if high_agreeableness_count > total_personas * 0.4:  # >40% highly agreeable
            alerts.append(BiasAlert(
                bias_type="sycophancy_risk",
                severity="medium",
                description=f"Too many highly agreeable personas ({high_agreeableness_count}/{total_personas})",
                affected_personas=[],
                mitigation_suggestions=[
                    "Reduce agreeableness scores for some personas",
                    "Add more personas with critical perspectives",
                    "Balance personality trait distributions"
                ]
            ))
        
        if low_criticism_count > total_personas * 0.6:  # >60% only positive
            alerts.append(BiasAlert(
                bias_type="sycophancy_risk",
                severity="high",
                description=f"Too many personas with only positive experiences ({low_criticism_count}/{total_personas})",
                affected_personas=[],
                mitigation_suggestions=[
                    "Add personas with mixed/negative experiences",
                    "Include realistic service complaints",
                    "Generate more balanced brand perceptions"
                ]
            ))
        
        return alerts
    
    def calculate_sycophancy_index(self, personas: List[Dict[str, Any]]) -> float:
        """Calculate overall sycophancy index for persona batch"""
        if not personas:
            return 0.0
        
        sycophancy_factors = []
        
        for persona in personas:
            characteristics = persona.get("characteristics", {})
            
            # Factor 1: Excessive agreeableness
            agreeableness = characteristics.get("personality_agreeableness", 5)
            agreeableness_factor = min((agreeableness - 5) / 5, 1.0) if agreeableness > 5 else 0
            
            # Factor 2: Only positive experiences
            service_exp = characteristics.get("customer_service_experience", "Regular")
            brand_perception = characteristics.get("brand_perception_tigo", "Neutral")
            
            positive_exp_factor = 0
            if service_exp in ["Excelente", "Buena"]:
                positive_exp_factor += 0.5
            if brand_perception in ["Muy positiva", "Positiva"]:
                positive_exp_factor += 0.5
            
            # Factor 3: High loyalty without criticism
            loyalty = characteristics.get("operator_loyalty", 5)
            recommendation = characteristics.get("recommendation_likelihood", 5)
            
            loyalty_factor = 0
            if loyalty > 8 and recommendation > 8:
                loyalty_factor = 0.7
            
            # Combine factors
            persona_sycophancy = np.mean([agreeableness_factor, positive_exp_factor, loyalty_factor])
            sycophancy_factors.append(persona_sycophancy)
        
        return np.mean(sycophancy_factors)


class BiasDetectionFramework:
    """Comprehensive bias detection and mitigation framework"""
    
    def __init__(self, honduras_demographics: Dict[str, Any]):
        self.stereotype_detector = StereotypeDetector()
        self.demographic_validator = DemographicValidator(honduras_demographics)
        self.sycophancy_detector = SycophancyDetector()
        
        # Validation thresholds
        self.validation_thresholds = {
            "diversity_score": 0.7,
            "sycophancy_index": 0.3,
            "demographic_alignment": 0.85,
            "stereotype_risk": 0.2
        }
    
    def comprehensive_bias_analysis(self, personas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform comprehensive bias analysis on persona batch"""
        analysis_results = {
            "timestamp": datetime.now().isoformat(),
            "total_personas": len(personas),
            "alerts": [],
            "metrics": {},
            "validation_passed": False,
            "recommendations": [],
            "detailed_analysis": {}
        }
        
        # 1. Stereotype detection
        stereotype_alerts = self.stereotype_detector.detect_stereotypes_in_batch(personas)
        analysis_results["alerts"].extend(stereotype_alerts)
        
        # 2. Demographic validation  
        demographic_alerts = self.demographic_validator.validate_demographic_distribution(personas)
        analysis_results["alerts"].extend(demographic_alerts)
        
        # 3. Sycophancy detection
        sycophancy_alerts = self.sycophancy_detector.detect_sycophancy_in_batch(personas)
        analysis_results["alerts"].extend(sycophancy_alerts)
        
        # 4. Calculate metrics
        analysis_results["metrics"] = self._calculate_comprehensive_metrics(personas)
        
        # 5. Overall validation
        analysis_results["validation_passed"] = self._validate_overall_quality(
            analysis_results["metrics"], analysis_results["alerts"]
        )
        
        # 6. Generate recommendations
        analysis_results["recommendations"] = self._generate_mitigation_recommendations(
            analysis_results["alerts"], analysis_results["metrics"]
        )
        
        # 7. Detailed analysis by category
        analysis_results["detailed_analysis"] = self._generate_detailed_analysis(personas)
        
        return analysis_results
    
    def _calculate_comprehensive_metrics(self, personas: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate comprehensive quality metrics"""
        metrics = {}
        
        # Diversity score
        metrics["diversity_score"] = self._calculate_diversity_score(personas)
        
        # Sycophancy index
        metrics["sycophancy_index"] = self.sycophancy_detector.calculate_sycophancy_index(personas)
        
        # Demographic alignment score
        metrics["demographic_alignment"] = self._calculate_demographic_alignment(personas)
        
        # Stereotype risk score
        metrics["stereotype_risk"] = self._calculate_stereotype_risk(personas)
        
        # Counter-stereotypical rate
        counter_stereotypical = sum(1 for p in personas if p.get("counter_stereotypical", False))
        metrics["counter_stereotypical_rate"] = counter_stereotypical / len(personas) if personas else 0
        
        # Human-like imperfection rate
        with_imperfections = sum(1 for p in personas if "human_imperfections" in p)
        metrics["human_imperfection_rate"] = with_imperfections / len(personas) if personas else 0
        
        return metrics
    
    def _calculate_diversity_score(self, personas: List[Dict[str, Any]]) -> float:
        """Calculate overall diversity score"""
        if not personas:
            return 0.0
        
        diversity_scores = []
        
        # Key characteristics for diversity calculation
        key_characteristics = [
            "age", "gender", "education_level", "income_bracket",
            "geographic_region", "service_type", "current_operator"
        ]
        
        for characteristic in key_characteristics:
            values = []
            for persona in personas:
                value = persona.get("characteristics", {}).get(characteristic)
                if value is not None:
                    values.append(str(value))
            
            if values:
                unique_values = len(set(values))
                total_values = len(values)
                char_diversity = unique_values / total_values
                diversity_scores.append(char_diversity)
        
        return np.mean(diversity_scores) if diversity_scores else 0.0
    
    def _calculate_demographic_alignment(self, personas: List[Dict[str, Any]]) -> float:
        """Calculate alignment with Honduras demographics"""
        if not personas:
            return 0.0
        
        alignment_scores = []
        
        # Age alignment
        age_alignment = self._calculate_age_alignment(personas)
        alignment_scores.append(age_alignment)
        
        # Gender alignment
        gender_alignment = self._calculate_gender_alignment(personas)
        alignment_scores.append(gender_alignment)
        
        # Income alignment
        income_alignment = self._calculate_income_alignment(personas)
        alignment_scores.append(income_alignment)
        
        return np.mean(alignment_scores)
    
    def _calculate_age_alignment(self, personas: List[Dict[str, Any]]) -> float:
        """Calculate age distribution alignment"""
        age_groups = defaultdict(int)
        total = len(personas)
        
        for persona in personas:
            age = persona.get("characteristics", {}).get("age", 30)
            age_group = self._get_age_group(age)
            age_groups[age_group] += 1
        
        # Compare with expected distribution
        expected = self.demographic_validator.honduras_demographics.get("age_distribution", {})
        
        alignment_score = 0.0
        for age_group, expected_pct in expected.items():
            actual_pct = age_groups.get(age_group, 0) / total if total > 0 else 0
            # Penalize large deviations
            deviation = abs(actual_pct - expected_pct)
            alignment_score += max(0, 1 - (deviation / expected_pct)) if expected_pct > 0 else 0
        
        return alignment_score / len(expected) if expected else 0.0
    
    def _calculate_gender_alignment(self, personas: List[Dict[str, Any]]) -> float:
        """Calculate gender distribution alignment"""
        gender_counts = defaultdict(int)
        total = len(personas)
        
        for persona in personas:
            gender = persona.get("characteristics", {}).get("gender", "")
            if gender:
                gender_counts[gender] += 1
        
        expected = self.demographic_validator.honduras_demographics.get("gender_distribution", {})
        
        alignment_score = 0.0
        for gender, expected_pct in expected.items():
            actual_pct = gender_counts.get(gender, 0) / total if total > 0 else 0
            deviation = abs(actual_pct - expected_pct)
            alignment_score += max(0, 1 - (deviation / expected_pct)) if expected_pct > 0 else 0
        
        return alignment_score / len(expected) if expected else 0.0
    
    def _calculate_income_alignment(self, personas: List[Dict[str, Any]]) -> float:
        """Calculate income distribution alignment"""
        income_counts = defaultdict(int)
        total = len(personas)
        
        for persona in personas:
            income = persona.get("characteristics", {}).get("income_bracket", "")
            if income:
                income_counts[income] += 1
        
        expected = self.demographic_validator.honduras_demographics.get("income_distribution", {})
        
        alignment_score = 0.0
        for income_bracket, expected_pct in expected.items():
            actual_pct = income_counts.get(income_bracket, 0) / total if total > 0 else 0
            deviation = abs(actual_pct - expected_pct)
            alignment_score += max(0, 1 - (deviation / expected_pct)) if expected_pct > 0 else 0
        
        return alignment_score / len(expected) if expected else 0.0
    
    def _calculate_stereotype_risk(self, personas: List[Dict[str, Any]]) -> float:
        """Calculate overall stereotype risk"""
        if not personas:
            return 0.0
        
        risk_scores = []
        
        for persona in personas:
            characteristics = persona.get("characteristics", {})
            persona_risk = 0.0
            
            # Check for stereotypical patterns
            for correlation_id, correlation_def in self.stereotype_detector.problematic_correlations.items():
                if correlation_def["pattern"](characteristics):
                    persona_risk += 0.2
            
            # Cap at 1.0
            risk_scores.append(min(persona_risk, 1.0))
        
        return np.mean(risk_scores)
    
    def _validate_overall_quality(self, metrics: Dict[str, float], 
                                alerts: List[BiasAlert]) -> bool:
        """Validate overall quality against thresholds"""
        # Check critical alerts
        critical_alerts = [a for a in alerts if a.severity == "critical"]
        if critical_alerts:
            return False
        
        # Check high-severity alerts
        high_severity_alerts = [a for a in alerts if a.severity == "high"]
        if len(high_severity_alerts) > 2:  # More than 2 high-severity alerts
            return False
        
        # Check metrics against thresholds
        for metric, threshold in self.validation_thresholds.items():
            if metric in metrics:
                if metric in ["diversity_score", "demographic_alignment"]:
                    # Higher is better
                    if metrics[metric] < threshold:
                        return False
                else:
                    # Lower is better (sycophancy_index, stereotype_risk)
                    if metrics[metric] > threshold:
                        return False
        
        return True
    
    def _generate_mitigation_recommendations(self, alerts: List[BiasAlert], 
                                           metrics: Dict[str, float]) -> List[str]:
        """Generate specific mitigation recommendations"""
        recommendations = []
        
        # Recommendations based on alerts
        for alert in alerts:
            recommendations.extend(alert.mitigation_suggestions)
        
        # Recommendations based on metrics
        if metrics.get("diversity_score", 0) < 0.7:
            recommendations.append("Increase diversity in key characteristics")
        
        if metrics.get("sycophancy_index", 0) > 0.3:
            recommendations.append("Reduce artificial agreeableness in personas")
        
        if metrics.get("counter_stereotypical_rate", 0) < 0.25:
            recommendations.append("Generate more counter-stereotypical personas")
        
        if metrics.get("human_imperfection_rate", 0) < 0.15:
            recommendations.append("Add more realistic human imperfections")
        
        # Remove duplicates
        return list(set(recommendations))
    
    def _generate_detailed_analysis(self, personas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate detailed analysis by category"""
        analysis = {
            "demographic_breakdown": self._analyze_demographic_breakdown(personas),
            "personality_distribution": self._analyze_personality_distribution(personas),
            "telecom_behavior_patterns": self._analyze_telecom_patterns(personas),
            "bias_risk_by_group": self._analyze_bias_risk_by_group(personas)
        }
        
        return analysis
    
    def _analyze_demographic_breakdown(self, personas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze demographic breakdown"""
        breakdown = {
            "age_groups": defaultdict(int),
            "gender_distribution": defaultdict(int),
            "education_levels": defaultdict(int),
            "income_brackets": defaultdict(int),
            "geographic_regions": defaultdict(int)
        }
        
        for persona in personas:
            characteristics = persona.get("characteristics", {})
            
            # Age groups
            age = characteristics.get("age", 30)
            age_group = self._get_age_group(age)
            breakdown["age_groups"][age_group] += 1
            
            # Other demographics
            gender = characteristics.get("gender", "")
            if gender:
                breakdown["gender_distribution"][gender] += 1
            
            education = characteristics.get("education_level", "")
            if education:
                breakdown["education_levels"][education] += 1
            
            income = characteristics.get("income_bracket", "")
            if income:
                breakdown["income_brackets"][income] += 1
            
            region = characteristics.get("geographic_region", "")
            if region:
                breakdown["geographic_regions"][region] += 1
        
        # Convert to percentages
        total = len(personas)
        for category in breakdown:
            for key in breakdown[category]:
                breakdown[category][key] = {
                    "count": breakdown[category][key],
                    "percentage": breakdown[category][key] / total if total > 0 else 0
                }
        
        return dict(breakdown)
    
    def _analyze_personality_distribution(self, personas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze personality trait distributions"""
        traits = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]
        
        distribution = {}
        
        for trait in traits:
            trait_name = f"personality_{trait}"
            values = []
            
            for persona in personas:
                value = persona.get("characteristics", {}).get(trait_name, 5)
                values.append(value)
            
            if values:
                distribution[trait] = {
                    "mean": np.mean(values),
                    "std": np.std(values),
                    "min": min(values),
                    "max": max(values),
                    "distribution": {
                        "low (1-3)": sum(1 for v in values if v <= 3) / len(values),
                        "medium (4-7)": sum(1 for v in values if 4 <= v <= 7) / len(values),
                        "high (8-10)": sum(1 for v in values if v >= 8) / len(values)
                    }
                }
        
        return distribution
    
    def _analyze_telecom_patterns(self, personas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze telecom-specific behavior patterns"""
        patterns = {
            "service_types": defaultdict(int),
            "operators": defaultdict(int),
            "spending_levels": defaultdict(int),
            "brand_perceptions": defaultdict(int)
        }
        
        for persona in personas:
            characteristics = persona.get("characteristics", {})
            
            service_type = characteristics.get("service_type", "")
            if service_type:
                patterns["service_types"][service_type] += 1
            
            operator = characteristics.get("current_operator", "")
            if operator:
                patterns["operators"][operator] += 1
            
            spending = characteristics.get("monthly_spend", "")
            if spending:
                patterns["spending_levels"][spending] += 1
            
            perception = characteristics.get("brand_perception_tigo", "")
            if perception:
                patterns["brand_perceptions"][perception] += 1
        
        # Convert to percentages
        total = len(personas)
        for category in patterns:
            for key in patterns[category]:
                patterns[category][key] = {
                    "count": patterns[category][key],
                    "percentage": patterns[category][key] / total if total > 0 else 0
                }
        
        return dict(patterns)
    
    def _analyze_bias_risk_by_group(self, personas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze bias risk by demographic groups"""
        risk_analysis = {}
        
        # Analyze by age group
        age_groups = defaultdict(list)
        for persona in personas:
            age = persona.get("characteristics", {}).get("age", 30)
            age_group = self._get_age_group(age)
            age_groups[age_group].append(persona)
        
        risk_analysis["by_age_group"] = {}
        for age_group, group_personas in age_groups.items():
            group_sycophancy = self.sycophancy_detector.calculate_sycophancy_index(group_personas)
            risk_analysis["by_age_group"][age_group] = {
                "count": len(group_personas),
                "sycophancy_index": group_sycophancy,
                "risk_level": "high" if group_sycophancy > 0.5 else "medium" if group_sycophancy > 0.3 else "low"
            }
        
        return risk_analysis
    
    def _get_age_group(self, age: int) -> str:
        """Convert age to age group"""
        if age <= 25:
            return "18-25"
        elif age <= 35:
            return "26-35"
        elif age <= 50:
            return "36-50"
        elif age <= 65:
            return "51-65"
        else:
            return "65+"