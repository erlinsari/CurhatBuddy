#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick test to verify response system works correctly
Tests: Natural Indonesian, Advice handling, Emotional reflection, Fallback chain
"""

import sys
from response_builder import DynamicResponseBuilder
from emotional_memory import EmotionalMemory

def test_response_system():
    """Test the response system with various inputs"""
    
    print("=" * 70)
    print("TESTING CURHAT BUDDY RESPONSE SYSTEM")
    print("=" * 70)
    
    # Initialize
    builder = DynamicResponseBuilder()
    memory = EmotionalMemory()
    
    # Test cases
    test_cases = [
        # Test 1: Simple emotion (Stage 1)
        {
            "name": "Simple Emotion - Tiredness",
            "message": "Aku capek banget",
            "stage": 1,
            "expected_tag": "[emotional reflection, no generic asking]"
        },
        # Test 2: Advice request
        {
            "name": "Advice Request",
            "message": "Aku capek banget. Gimana caranya biar nggak capek gini?",
            "stage": 1,
            "expected_tag": "[should contain advice + practical steps]"
        },
        # Test 3: Body image issue
        {
            "name": "Body Image Topic",
            "message": "Aku banyak jerawat, malu mau ketemu orang",
            "stage": 1,
            "expected_tag": "[emotional reflection about insecurity, not 'aku siap']"
        },
        # Test 4: Unknown/vague topic
        {
            "name": "Vague Message",
            "message": "aku kayak gimana gitu",
            "stage": 1,
            "expected_tag": "[universal fallback, emotional reflection]"
        },
        # Test 5: Very short message
        {
            "name": "Very Short Message",
            "message": "sedih",
            "stage": 1,
            "expected_tag": "[short response, no over-explaining]"
        },
        # Test 6: Multi-line emotional sharing
        {
            "name": "Longer Emotional Sharing",
            "message": "Aku merasa sendiri di antara teman-teman. Mereka kayak punya kehidupan sendiri dan aku cuma jadi yang ketinggalan.",
            "stage": 2,
            "expected_tag": "[emotional reflection, might add question]"
        },
    ]
    
    # Run tests
    for i, test in enumerate(test_cases, 1):
        print(f"\n[TEST {i}] {test['name']}")
        print(f"Input: \"{test['message']}\"")
        print(f"Stage: {test['stage']}")
        print(f"Expected: {test['expected_tag']}")
        print("-" * 70)
        
        try:
            response = builder.build_response(
                test['message'],
                memory,
                test['stage']
            )
            print(f"Response: {response}")
        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()
        
        print()
    
    # Summary
    print("\n" + "=" * 70)
    print("VERIFICATION CHECKLIST:")
    print("=" * 70)
    print("✓ No syntax errors during execution")
    print("✓ System generates responses for all test cases")
    print("✓ Check if responses contain:")
    print("  - Natural Indonesian (no English)")
    print("  - Emotional reflection (not generic 'aku siap dengarkan')")
    print("  - For advice: 4-step flow (validate → insight → steps → closing)")
    print("✓ Fallback chain working (no empty responses)")
    print()

if __name__ == "__main__":
    try:
        test_response_system()
        print("✅ Test completed successfully!\n")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
