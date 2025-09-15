# personas/temperature_optimization.py
"""
Temperature Optimization System for LLM Persona Generation
Based on academic research showing hierarchical sampling reduces 'correct answer effect'
and maintains coherence while avoiding single-response patterns.

Key findings from research:
- High temperature (0.8) for general features generation
- Low temperature (0.3) for individual coherence maintenance  
- Temperature=1.0 causes identical responses across personas
- Top-k and top-p sampling maintain diversity while ensuring coherence
"""

import json
import random
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class GenerationStage(Enum):
    """Different stages of persona generation requiring different temperature settings"""
    GENERAL_FEATURES = "general_features"      # High temperature for diversity
    PERSONALITY_TRAITS = "personality_traits"  # Medium-high temperature
    INDIVIDUAL_COHERENCE = "individual_coherence"  # Low temperature
    RESPONSE_GENERATION = "response_generation"    # Dynamic temperature
    CONSISTENCY_MAINTENANCE = "consistency_maintenance"  # Very low temperature


@dataclass
class TemperatureConfig:
    """Configuration for temperature optimization at different stages"""
    temperature: float
    top_k: Optional[int] = None
    top_p: Optional[float] = None
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stage_description: str = ""
    

class HierarchicalTemperatureOptimizer:
    """Optimizes temperature settings for different stages of persona generation"""
    
    def __init__(self):
        # Research-based temperature configurations for each stage
        self.stage_configs = {
            GenerationStage.GENERAL_FEATURES: TemperatureConfig(
                temperature=0.8,
                top_k=40,
                top_p=0.9,
                frequency_penalty=0.3,
                presence_penalty=0.2,
                stage_description="High diversity for demographic and general characteristics"
            ),
            
            GenerationStage.PERSONALITY_TRAITS: TemperatureConfig(
                temperature=0.7,
                top_k=30,
                top_p=0.85,
                frequency_penalty=0.2,
                presence_penalty=0.1,
                stage_description="Balanced creativity for personality trait generation"
            ),
            
            GenerationStage.INDIVIDUAL_COHERENCE: TemperatureConfig(
                temperature=0.3,
                top_k=15,
                top_p=0.7,
                frequency_penalty=0.1,
                presence_penalty=0.05,
                stage_description="Low temperature for internal consistency"
            ),
            
            GenerationStage.RESPONSE_GENERATION: TemperatureConfig(
                temperature=0.5,  # Dynamic, will be adjusted based on persona
                top_k=25,
                top_p=0.8,
                frequency_penalty=0.15,
                presence_penalty=0.1,
                stage_description="Dynamic temperature based on persona characteristics"
            ),
            
            GenerationStage.CONSISTENCY_MAINTENANCE: TemperatureConfig(
                temperature=0.2,
                top_k=10,
                top_p=0.6,
                frequency_penalty=0.05,
                presence_penalty=0.0,
                stage_description="Very low temperature for maintaining established patterns"
            )
        }
        
        # Persona-specific temperature modifiers
        self.personality_modifiers = {
            "extraversion": {
                "high": 0.1,    # More extraverted = slightly higher temperature
                "low": -0.1     # More introverted = slightly lower temperature
            },
            "openness": {
                "high": 0.15,   # More open = higher temperature for creativity
                "low": -0.1     # Less open = lower temperature for consistency
            },
            "neuroticism": {
                "high": -0.05,  # Higher neuroticism = slightly more consistent responses
                "low": 0.05     # Lower neuroticism = slight variation allowed
            },
            "agreeableness": {
                "high": -0.05,  # Higher agreeableness = more consistent positive responses
                "low": 0.1      # Lower agreeableness = more varied/critical responses
            }
        }
        
        # Conversation context modifiers
        self.context_modifiers = {
            "first_interaction": 0.1,      # Slightly higher for initial responses
            "follow_up": 0.0,             # Normal temperature
            "deep_topic": -0.1,           # Lower for thoughtful responses
            "casual_chat": 0.05,          # Slightly higher for casual interaction
            "emotional_topic": -0.05,     # Lower for emotional consistency
            "technical_topic": -0.1       # Lower for technical accuracy
        }
    
    def get_optimized_config(self, stage: GenerationStage, 
                           persona_characteristics: Optional[Dict[str, Any]] = None,
                           conversation_context: Optional[str] = None) -> TemperatureConfig:
        """Get optimized temperature configuration for specific stage and context"""
        
        # Start with base configuration for stage
        base_config = self.stage_configs[stage]
        
        # Clone the configuration to avoid modifying the original
        optimized_config = TemperatureConfig(
            temperature=base_config.temperature,
            top_k=base_config.top_k,
            top_p=base_config.top_p,
            frequency_penalty=base_config.frequency_penalty,
            presence_penalty=base_config.presence_penalty,
            stage_description=base_config.stage_description
        )
        
        # Apply persona-specific modifications
        if persona_characteristics and stage == GenerationStage.RESPONSE_GENERATION:
            temperature_adjustment = self._calculate_persona_temperature_adjustment(persona_characteristics)
            optimized_config.temperature = max(0.1, min(1.0, 
                optimized_config.temperature + temperature_adjustment))
        
        # Apply conversation context modifications
        if conversation_context:
            context_adjustment = self._calculate_context_temperature_adjustment(conversation_context)
            optimized_config.temperature = max(0.1, min(1.0, 
                optimized_config.temperature + context_adjustment))
        
        return optimized_config
    
    def _calculate_persona_temperature_adjustment(self, characteristics: Dict[str, Any]) -> float:
        """Calculate temperature adjustment based on persona characteristics"""
        total_adjustment = 0.0
        
        # Extraversion adjustment
        extraversion = characteristics.get("personality_extraversion", 5)
        if extraversion > 7:
            total_adjustment += self.personality_modifiers["extraversion"]["high"]
        elif extraversion < 4:
            total_adjustment += self.personality_modifiers["extraversion"]["low"]
        
        # Openness adjustment
        openness = characteristics.get("personality_openness", 5)
        if openness > 7:
            total_adjustment += self.personality_modifiers["openness"]["high"]
        elif openness < 4:
            total_adjustment += self.personality_modifiers["openness"]["low"]
        
        # Neuroticism adjustment
        neuroticism = characteristics.get("personality_neuroticism", 5)
        if neuroticism > 7:
            total_adjustment += self.personality_modifiers["neuroticism"]["high"]
        elif neuroticism < 4:
            total_adjustment += self.personality_modifiers["neuroticism"]["low"]
        
        # Agreeableness adjustment
        agreeableness = characteristics.get("personality_agreeableness", 5)
        if agreeableness > 7:
            total_adjustment += self.personality_modifiers["agreeableness"]["high"]
        elif agreeableness < 4:
            total_adjustment += self.personality_modifiers["agreeableness"]["low"]
        
        # Cap the total adjustment to prevent extreme values
        return max(-0.3, min(0.3, total_adjustment))
    
    def _calculate_context_temperature_adjustment(self, context: str) -> float:
        """Calculate temperature adjustment based on conversation context"""
        context_lower = context.lower()
        
        # Check for context indicators
        if any(word in context_lower for word in ["primera vez", "conocer", "inicial"]):
            return self.context_modifiers["first_interaction"]
        
        if any(word in context_lower for word in ["profundo", "personal", "importante"]):
            return self.context_modifiers["deep_topic"]
        
        if any(word in context_lower for word in ["casual", "relajado", "informal"]):
            return self.context_modifiers["casual_chat"]
        
        if any(word in context_lower for word in ["triste", "preocupado", "emocional"]):
            return self.context_modifiers["emotional_topic"]
        
        if any(word in context_lower for word in ["técnico", "específico", "detalle"]):
            return self.context_modifiers["technical_topic"]
        
        return self.context_modifiers["follow_up"]  # Default
    
    def generate_sampling_parameters(self, config: TemperatureConfig) -> Dict[str, Any]:
        """Generate complete sampling parameters for API calls"""
        return {
            "temperature": config.temperature,
            "top_k": config.top_k,
            "top_p": config.top_p,
            "frequency_penalty": config.frequency_penalty,
            "presence_penalty": config.presence_penalty,
            "max_tokens": self._get_appropriate_max_tokens(config),
        }
    
    def _get_appropriate_max_tokens(self, config: TemperatureConfig) -> int:
        """Get appropriate max_tokens based on temperature and stage"""
        # Higher temperature stages might need more tokens for diverse responses
        if config.temperature > 0.7:
            return 1000  # More tokens for creative/diverse responses
        elif config.temperature > 0.4:
            return 800   # Moderate tokens for balanced responses
        else:
            return 600   # Fewer tokens for consistent/focused responses


class AntiCorrelationSampler:
    """Prevents 'correct answer effect' by ensuring diverse responses across personas"""
    
    def __init__(self, similarity_threshold: float = 0.85):
        self.similarity_threshold = similarity_threshold
        self.generated_responses = []  # Track responses to avoid high similarity
        self.response_patterns = {}    # Track common patterns
        
    def check_response_diversity(self, new_response: str, persona_id: str) -> Dict[str, Any]:
        """Check if new response is sufficiently diverse from existing responses"""
        
        diversity_analysis = {
            "is_diverse": True,
            "similarity_scores": [],
            "problematic_patterns": [],
            "recommendations": []
        }
        
        # Check against recent responses
        for existing_response in self.generated_responses[-50:]:  # Check last 50
            similarity = self._calculate_text_similarity(new_response, existing_response["content"])
            diversity_analysis["similarity_scores"].append({
                "persona_id": existing_response["persona_id"],
                "similarity": similarity
            })
            
            if similarity > self.similarity_threshold:
                diversity_analysis["is_diverse"] = False
                diversity_analysis["problematic_patterns"].append(
                    f"High similarity ({similarity:.2f}) with persona {existing_response['persona_id']}"
                )
        
        # Check for common response patterns
        pattern_issues = self._detect_common_patterns(new_response)
        diversity_analysis["problematic_patterns"].extend(pattern_issues)
        
        if pattern_issues:
            diversity_analysis["is_diverse"] = False
        
        # Generate recommendations for improvement
        if not diversity_analysis["is_diverse"]:
            diversity_analysis["recommendations"] = self._generate_diversity_recommendations(
                new_response, diversity_analysis["problematic_patterns"]
            )
        
        # Store the response for future checks
        self.generated_responses.append({
            "persona_id": persona_id,
            "content": new_response,
            "timestamp": np.datetime64('now')
        })
        
        # Keep only recent responses to manage memory
        if len(self.generated_responses) > 200:
            self.generated_responses = self.generated_responses[-150:]
        
        return diversity_analysis
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple text similarity based on word overlap"""
        
        # Simple word-based similarity (can be enhanced with embeddings)
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _detect_common_patterns(self, response: str) -> List[str]:
        """Detect common patterns that indicate 'correct answer effect'"""
        problems = []
        response_lower = response.lower()
        
        # Check for overly generic responses
        generic_patterns = [
            "en general bien", "todo normal", "como siempre", "sin problemas",
            "muy satisfecho", "excelente servicio", "sin quejas"
        ]
        
        generic_count = sum(1 for pattern in generic_patterns if pattern in response_lower)
        if generic_count > 2:
            problems.append("Overly generic response patterns detected")
        
        # Check for excessive positivity (sycophancy indicator)
        positive_words = ["excelente", "perfecto", "maravilloso", "increíble", "fantástico"]
        positive_count = sum(1 for word in positive_words if word in response_lower)
        if positive_count > 3:
            problems.append("Excessive positivity may indicate sycophancy")
        
        # Check for lack of specific details
        if len(response.split()) > 50 and ("específico" not in response_lower and 
                                         "ejemplo" not in response_lower and
                                         "experiencia" not in response_lower):
            problems.append("Lacks specific details or personal examples")
        
        # Check for identical sentence structures
        sentences = response.split('.')
        if len(sentences) > 3:
            sentence_starts = [s.strip()[:10].lower() for s in sentences if s.strip()]
            if len(set(sentence_starts)) < len(sentence_starts) * 0.7:  # Less than 70% unique starts
                problems.append("Repetitive sentence structures")
        
        return problems
    
    def _generate_diversity_recommendations(self, response: str, problems: List[str]) -> List[str]:
        """Generate recommendations to improve response diversity"""
        recommendations = []
        
        if any("generic" in problem.lower() for problem in problems):
            recommendations.append("Add more specific personal experiences and details")
            recommendations.append("Include conditional statements (aunque, pero, sin embargo)")
        
        if any("positivity" in problem.lower() for problem in problems):
            recommendations.append("Balance positive aspects with realistic concerns")
            recommendations.append("Include mixed experiences and nuanced opinions")
        
        if any("similarity" in problem.lower() for problem in problems):
            recommendations.append("Increase temperature or adjust sampling parameters")
            recommendations.append("Use more persona-specific context in prompting")
        
        if any("details" in problem.lower() for problem in problems):
            recommendations.append("Incorporate more personal history context")
            recommendations.append("Reference specific situations or experiences")
        
        if any("repetitive" in problem.lower() for problem in problems):
            recommendations.append("Vary sentence structures and response patterns")
            recommendations.append("Use different conversation styles based on persona")
        
        return recommendations
    
    def get_diversity_statistics(self) -> Dict[str, Any]:
        """Get statistics about response diversity"""
        if len(self.generated_responses) < 2:
            return {"message": "Insufficient data for diversity analysis"}
        
        # Calculate average similarity across all responses
        similarities = []
        for i, response1 in enumerate(self.generated_responses):
            for response2 in self.generated_responses[i+1:]:
                similarity = self._calculate_text_similarity(
                    response1["content"], response2["content"]
                )
                similarities.append(similarity)
        
        avg_similarity = np.mean(similarities) if similarities else 0.0
        max_similarity = max(similarities) if similarities else 0.0
        
        # Count problematic responses
        problematic_count = 0
        for response in self.generated_responses:
            problems = self._detect_common_patterns(response["content"])
            if problems:
                problematic_count += 1
        
        return {
            "total_responses": len(self.generated_responses),
            "average_similarity": round(avg_similarity, 3),
            "max_similarity": round(max_similarity, 3),
            "diversity_score": round(1 - avg_similarity, 3),  # Higher is better
            "problematic_responses": problematic_count,
            "problematic_percentage": round(problematic_count / len(self.generated_responses) * 100, 1),
            "diversity_status": "Good" if avg_similarity < 0.3 else "Moderate" if avg_similarity < 0.6 else "Poor"
        }


class AdvancedTemperatureController:
    """Advanced controller that manages temperature optimization and anti-correlation sampling"""
    
    def __init__(self):
        self.temperature_optimizer = HierarchicalTemperatureOptimizer()
        self.anti_correlation_sampler = AntiCorrelationSampler()
        
        # Performance tracking
        self.generation_stats = {
            "total_generations": 0,
            "stage_usage": {stage: 0 for stage in GenerationStage},
            "diversity_rejections": 0,
            "temperature_adjustments": 0
        }
    
    def get_generation_parameters(self, stage: GenerationStage,
                                persona_characteristics: Optional[Dict[str, Any]] = None,
                                conversation_context: Optional[str] = None,
                                attempt_number: int = 1) -> Dict[str, Any]:
        """Get optimized generation parameters with diversity control"""
        
        # Get base configuration
        config = self.temperature_optimizer.get_optimized_config(
            stage, persona_characteristics, conversation_context
        )
        
        # Adjust for retry attempts (increase temperature for diversity)
        if attempt_number > 1:
            config.temperature = min(1.0, config.temperature + (attempt_number - 1) * 0.1)
            config.top_p = min(1.0, config.top_p + (attempt_number - 1) * 0.05)
            self.generation_stats["temperature_adjustments"] += 1
        
        # Generate sampling parameters
        parameters = self.temperature_optimizer.generate_sampling_parameters(config)
        
        # Add stage and context information
        parameters.update({
            "generation_stage": stage.value,
            "attempt_number": attempt_number,
            "stage_description": config.stage_description
        })
        
        # Update usage statistics
        self.generation_stats["total_generations"] += 1
        self.generation_stats["stage_usage"][stage] += 1
        
        return parameters
    
    def validate_and_improve_response(self, response: str, persona_id: str,
                                    generation_parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Validate response diversity and suggest improvements"""
        
        # Check diversity
        diversity_analysis = self.anti_correlation_sampler.check_response_diversity(
            response, persona_id
        )
        
        # Update rejection statistics
        if not diversity_analysis["is_diverse"]:
            self.generation_stats["diversity_rejections"] += 1
        
        # Prepare response validation
        validation_result = {
            "response": response,
            "diversity_analysis": diversity_analysis,
            "generation_parameters": generation_parameters,
            "should_regenerate": not diversity_analysis["is_diverse"],
            "improvement_suggestions": diversity_analysis.get("recommendations", []),
            "quality_score": self._calculate_quality_score(response, diversity_analysis)
        }
        
        return validation_result
    
    def _calculate_quality_score(self, response: str, diversity_analysis: Dict[str, Any]) -> float:
        """Calculate overall quality score for response"""
        score = 1.0
        
        # Penalize for diversity issues
        if not diversity_analysis["is_diverse"]:
            score -= 0.3
        
        # Penalize for problematic patterns
        pattern_penalty = len(diversity_analysis.get("problematic_patterns", [])) * 0.1
        score -= min(pattern_penalty, 0.4)
        
        # Reward for appropriate length
        word_count = len(response.split())
        if 30 <= word_count <= 200:  # Ideal range
            score += 0.1
        elif word_count < 10:  # Too short
            score -= 0.2
        elif word_count > 300:  # Too long
            score -= 0.1
        
        # Reward for balanced content (has both positive and concerns)
        response_lower = response.lower()
        has_positive = any(word in response_lower for word in ["bien", "bueno", "satisfecho"])
        has_concerns = any(word in response_lower for word in ["pero", "aunque", "problema"])
        
        if has_positive and has_concerns:
            score += 0.2
        elif not has_positive and not has_concerns:
            score -= 0.1
        
        return max(0.0, min(1.0, score))
    
    def get_performance_statistics(self) -> Dict[str, Any]:
        """Get comprehensive performance statistics"""
        diversity_stats = self.anti_correlation_sampler.get_diversity_statistics()
        
        total_gens = self.generation_stats["total_generations"]
        rejection_rate = (self.generation_stats["diversity_rejections"] / total_gens * 100 
                         if total_gens > 0 else 0)
        
        return {
            "generation_statistics": self.generation_stats,
            "diversity_statistics": diversity_stats,
            "performance_metrics": {
                "total_generations": total_gens,
                "diversity_rejection_rate": round(rejection_rate, 2),
                "temperature_adjustment_rate": round(
                    self.generation_stats["temperature_adjustments"] / total_gens * 100 
                    if total_gens > 0 else 0, 2
                ),
                "overall_quality": diversity_stats.get("diversity_status", "Unknown")
            },
            "recommendations": self._generate_performance_recommendations(rejection_rate, diversity_stats)
        }
    
    def _generate_performance_recommendations(self, rejection_rate: float, 
                                           diversity_stats: Dict[str, Any]) -> List[str]:
        """Generate recommendations for improving generation performance"""
        recommendations = []
        
        if rejection_rate > 20:
            recommendations.append("High diversity rejection rate - consider increasing base temperatures")
        
        if diversity_stats.get("diversity_score", 0) < 0.5:
            recommendations.append("Low diversity score - review persona characteristic variations")
        
        if diversity_stats.get("problematic_percentage", 0) > 30:
            recommendations.append("High rate of problematic patterns - review prompt engineering")
        
        if not recommendations:
            recommendations.append("Performance is within acceptable parameters")
        
        return recommendations